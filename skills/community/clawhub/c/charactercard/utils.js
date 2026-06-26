/**
 * SillyTavern Character Card Utilities
 * 完整的角色卡处理工具集
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * 检测文件格式
 */
function detectFileFormat(buffer) {
  // PNG: 89 50 4E 47 0D 0A 1A 0A
  if (buffer.length >= 8 &&
      buffer[0] === 0x89 && buffer[1] === 0x50 &&
      buffer[2] === 0x4E && buffer[3] === 0x47) {
    return 'png';
  }

  // JPEG: FF D8 FF
  if (buffer.length >= 3 &&
      buffer[0] === 0xFF && buffer[1] === 0xD8 && buffer[2] === 0xFF) {
    return 'jpeg';
  }

  // WEBP: RIFF ... WEBP
  if (buffer.length >= 12 &&
      buffer.toString('ascii', 0, 4) === 'RIFF' &&
      buffer.toString('ascii', 8, 12) === 'WEBP') {
    return 'webp';
  }

  // JSON: { 或 [
  const firstChar = buffer.toString('utf8', 0, 1);
  if (firstChar === '{' || firstChar === '[') {
    return 'json';
  }

  return 'unknown';
}

/**
 * 从 PNG 提取角色卡数据
 */
function extractCharaFromPNG(buffer) {
  // 验证 PNG 签名
  const pngSignature = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
  if (!buffer.slice(0, 8).equals(pngSignature)) {
    throw new Error('不是有效的 PNG 文件');
  }

  let offset = 8; // 跳过 PNG 签名

  while (offset < buffer.length) {
    // 读取 chunk 长度（4 字节，大端序）
    if (offset + 8 > buffer.length) break;
    const length = buffer.readUInt32BE(offset);
    offset += 4;

    // 读取 chunk 类型（4 字节）
    const type = buffer.toString('ascii', offset, offset + 4);
    offset += 4;

    // 检查是否为文本 chunk
    if (type === 'tEXt' || type === 'iTXt') {
      // 读取关键字（以 null 结尾）
      let keywordEnd = offset;
      while (keywordEnd < offset + length && buffer[keywordEnd] !== 0) {
        keywordEnd++;
      }

      const keyword = buffer.toString('utf8', offset, keywordEnd);

      if (keyword === 'chara') {
        // 提取数据（跳过 null 字节）
        const dataStart = keywordEnd + 1;
        const dataEnd = offset + length;

        if (dataStart >= dataEnd) {
          throw new Error('chara chunk 数据为空');
        }

        const data = buffer.toString('utf8', dataStart, dataEnd);

        // 尝试 base64 解码
        try {
          const decoded = Buffer.from(data, 'base64').toString('utf8');
          return JSON.parse(decoded);
        } catch (e) {
          // 如果 base64 解码失败，尝试直接解析
          try {
            return JSON.parse(data);
          } catch (e2) {
            throw new Error(`JSON 解析失败: ${e2.message}`);
          }
        }
      }
    }

    // 跳到下一个 chunk（数据 + 4 字节 CRC）
    offset += length + 4;

    // IEND chunk 表示文件结束
    if (type === 'IEND') break;
  }

  throw new Error('PNG 文件中未找到 chara 数据');
}

/**
 * 规范化角色卡数据（V1 → V2/V3）
 */
function normalizeCharacterCard(data) {
  // 已经是 V2/V3 格式
  if (data.spec === 'chara_card_v2' || data.spec === 'chara_card_v3') {
    return data;
  }

  // V1 转 V2
  return {
    spec: 'chara_card_v2',
    spec_version: '2.0',
    data: {
      name: data.name || '',
      description: data.description || '',
      personality: data.personality || '',
      scenario: data.scenario || '',
      first_mes: data.first_mes || '',
      mes_example: data.mes_example || '',
      creator_notes: data.creator_notes || '',
      system_prompt: data.system_prompt || '',
      post_history_instructions: data.post_history_instructions || '',
      tags: data.tags || [],
      creator: data.creator || '',
      character_version: data.character_version || '1.0',
      extensions: data.extensions || {},
      // 保留 character_book
      ...(data.character_book && { character_book: data.character_book })
    }
  };
}

/**
 * 检测并升级到 V3 格式
 */
function upgradeToV3(data) {
  const normalized = normalizeCharacterCard(data);

  // 检查是否有 V3 特有字段
  const hasV3Fields =
    normalized.data.alternate_greetings ||
    normalized.data.creator_notes_multilingual ||
    normalized.data.source ||
    normalized.data.group_only_greetings ||
    normalized.data.assets;

  if (hasV3Fields || normalized.spec === 'chara_card_v3') {
    return {
      ...normalized,
      spec: 'chara_card_v3',
      spec_version: '3.0',
      data: {
        ...normalized.data,
        alternate_greetings: normalized.data.alternate_greetings || [],
        creator_notes_multilingual: normalized.data.creator_notes_multilingual || {},
        source: normalized.data.source || '',
        group_only_greetings: normalized.data.group_only_greetings || [],
        creation_date: normalized.data.creation_date || Date.now(),
        modification_date: Date.now(),
        assets: normalized.data.assets || {}
      }
    };
  }

  return normalized;
}

/**
 * 验证角色卡数据
 */
function validateCharacterCard(data) {
  const errors = [];
  const warnings = [];

  // 获取实际数据（处理 V2/V3 的嵌套结构）
  const cardData = data.data || data;

  // 检查必需字段
  if (!cardData.name || cardData.name.trim() === '') {
    errors.push('缺少角色名称 (name)');
  }

  if (!cardData.description || cardData.description.trim() === '') {
    warnings.push('缺少角色描述 (description)');
  }

  // 检查字段类型
  if (cardData.tags && !Array.isArray(cardData.tags)) {
    errors.push('标签 (tags) 必须是数组');
  }

  if (cardData.extensions && typeof cardData.extensions !== 'object') {
    errors.push('扩展 (extensions) 必须是对象');
  }

  // V3 特有字段验证
  if (data.spec === 'chara_card_v3') {
    if (cardData.alternate_greetings && !Array.isArray(cardData.alternate_greetings)) {
      errors.push('备选问候 (alternate_greetings) 必须是数组');
    }

    if (cardData.creator_notes_multilingual && typeof cardData.creator_notes_multilingual !== 'object') {
      errors.push('多语言备注 (creator_notes_multilingual) 必须是对象');
    }
  }

  // 检查数据大小
  const jsonSize = JSON.stringify(data).length;
  if (jsonSize > 10 * 1024 * 1024) { // 10 MB
    warnings.push(`角色卡数据过大 (${(jsonSize / 1024 / 1024).toFixed(2)} MB)，建议 < 10 MB`);
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * 格式化显示角色信息
 */
function formatCharacterInfo(data) {
  const normalized = normalizeCharacterCard(data);
  const cardData = normalized.data;

  const lines = [];
  lines.push('📋 角色信息');
  lines.push('━━━━━━━━━━━━━━━━━━━━');
  lines.push(`• 名称：${cardData.name}`);
  lines.push(`• 规范：${normalized.spec} (${normalized.spec_version})`);

  if (cardData.creator) {
    lines.push(`• 创建者：${cardData.creator}`);
  }

  if (cardData.character_version) {
    lines.push(`• 版本：${cardData.character_version}`);
  }

  if (cardData.tags && cardData.tags.length > 0) {
    lines.push(`• 标签：${cardData.tags.join('、')}`);
  }

  lines.push('');
  lines.push('📖 描述');
  lines.push('━━━━━━━━━━━━━━━━━━━━');
  lines.push(cardData.description || '(无)');

  if (cardData.personality) {
    lines.push('');
    lines.push('🎭 人格');
    lines.push('━━━━━━━━━━━━━━━━━━━━');
    lines.push(cardData.personality);
  }

  if (cardData.scenario) {
    lines.push('');
    lines.push('🌍 场景');
    lines.push('━━━━━━━━━━━━━━━━━━━━');
    lines.push(cardData.scenario);
  }

  if (cardData.first_mes) {
    lines.push('');
    lines.push('💬 第一条消息');
    lines.push('━━━━━━━━━━━━━━━━━━━━');
    lines.push(`"${cardData.first_mes}"`);
  }

  if (cardData.mes_example) {
    lines.push('');
    lines.push('📝 示例对话');
    lines.push('━━━━━━━━━━━━━━━━━━━━');
    lines.push(cardData.mes_example);
  }

  // V3 特有字段
  if (normalized.spec === 'chara_card_v3') {
    if (cardData.alternate_greetings && cardData.alternate_greetings.length > 0) {
      lines.push('');
      lines.push('🔄 备选问候');
      lines.push('━━━━━━━━━━━━━━━━━━━━');
      cardData.alternate_greetings.forEach((greeting, i) => {
        lines.push(`${i + 1}. "${greeting}"`);
      });
    }

    if (cardData.source) {
      lines.push('');
      lines.push(`📚 来源：${cardData.source}`);
    }
  }

  // 世界书
  if (cardData.character_book && cardData.character_book.entries) {
    lines.push('');
    lines.push(`📚 世界书：${cardData.character_book.entries.length} 条目`);
  }

  return lines.join('\n');
}

/**
 * 计算 CRC32
 */
function calculateCRC32(buffer) {
  const table = [];
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let j = 0; j < 8; j++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[i] = c;
  }

  let crc = 0xFFFFFFFF;
  for (let i = 0; i < buffer.length; i++) {
    crc = table[(crc ^ buffer[i]) & 0xFF] ^ (crc >>> 8);
  }
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

/**
 * 将角色卡数据嵌入到 PNG
 */
function embedCharaInPNG(imageBuffer, characterData) {
  // 验证 PNG 签名
  const pngSignature = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
  if (!imageBuffer.slice(0, 8).equals(pngSignature)) {
    throw new Error('不是有效的 PNG 文件');
  }

  // 将角色数据转换为 base64
  const jsonStr = JSON.stringify(characterData);
  const base64Data = Buffer.from(jsonStr, 'utf8').toString('base64');

  // 创建 tEXt chunk
  const keyword = 'chara';
  const keywordBuffer = Buffer.from(keyword + '\0', 'utf8');
  const dataBuffer = Buffer.from(base64Data, 'utf8');

  const chunkDataLength = keywordBuffer.length + dataBuffer.length;
  const chunkData = Buffer.concat([keywordBuffer, dataBuffer]);

  // 创建完整的 chunk
  const chunk = Buffer.alloc(chunkDataLength + 12);

  // 写入 chunk 长度（不包括长度字段本身和 CRC）
  chunk.writeUInt32BE(chunkDataLength, 0);

  // 写入 chunk 类型
  chunk.write('tEXt', 4, 'ascii');

  // 写入数据
  chunkData.copy(chunk, 8);

  // 计算并写入 CRC（包括类型和数据，不包括长度）
  const crc = calculateCRC32(chunk.slice(4, 8 + chunkDataLength));
  chunk.writeUInt32BE(crc, 8 + chunkDataLength);

  // 找到 IEND chunk 的位置
  let iendIndex = -1;
  for (let i = 8; i < imageBuffer.length - 4; i++) {
    if (imageBuffer.toString('ascii', i, i + 4) === 'IEND') {
      iendIndex = i - 4; // IEND 前面的长度字段位置
      break;
    }
  }

  if (iendIndex === -1) {
    throw new Error('PNG 文件格式错误：未找到 IEND chunk');
  }

  // 在 IEND 之前插入 chunk
  return Buffer.concat([
    imageBuffer.slice(0, iendIndex),
    chunk,
    imageBuffer.slice(iendIndex)
  ]);
}

/**
 * 创建最小 PNG（1x1 透明像素）
 */
function createMinimalPNG() {
  // 1x1 透明 PNG
  return Buffer.from([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, // PNG 签名
    0x00, 0x00, 0x00, 0x0D, // IHDR 长度
    0x49, 0x48, 0x44, 0x52, // IHDR
    0x00, 0x00, 0x00, 0x01, // 宽度 1
    0x00, 0x00, 0x00, 0x01, // 高度 1
    0x08, 0x06, 0x00, 0x00, 0x00, // 位深度 8, 颜色类型 6 (RGBA)
    0x1F, 0x15, 0xC4, 0x89, // CRC
    0x00, 0x00, 0x00, 0x0A, // IDAT 长度
    0x49, 0x44, 0x41, 0x54, // IDAT
    0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00, 0x05, 0x00, 0x01, // 压缩数据
    0x0D, 0x0A, 0x2D, 0xB4, // CRC
    0x00, 0x00, 0x00, 0x00, // IEND 长度
    0x49, 0x45, 0x4E, 0x44, // IEND
    0xAE, 0x42, 0x60, 0x82  // CRC
  ]);
}

/**
 * 主函数：导入角色卡
 */
async function importCharacterCard(filePath) {
  const buffer = fs.readFileSync(filePath);
  const format = detectFileFormat(buffer);

  let characterData;

  if (format === 'png') {
    characterData = extractCharaFromPNG(buffer);
  } else if (format === 'json') {
    characterData = JSON.parse(buffer.toString('utf8'));
  } else {
    throw new Error(`不支持的文件格式: ${format}`);
  }

  // 规范化数据
  const normalized = normalizeCharacterCard(characterData);

  // 验证数据
  const validation = validateCharacterCard(normalized);

  return {
    data: normalized,
    validation,
    format,
    filePath
  };
}

/**
 * 主函数：导出角色卡为 PNG
 */
async function exportCharacterCardPNG(characterData, outputPath, avatarPath = null) {
  // 规范化数据
  const normalized = normalizeCharacterCard(characterData);

  // 验证数据
  const validation = validateCharacterCard(normalized);
  if (!validation.valid) {
    throw new Error(`角色卡数据验证失败:\n${validation.errors.join('\n')}`);
  }

  // 读取或创建头像
  let imageBuffer;
  if (avatarPath && fs.existsSync(avatarPath)) {
    imageBuffer = fs.readFileSync(avatarPath);
    const format = detectFileFormat(imageBuffer);
    if (format !== 'png') {
      throw new Error('头像必须是 PNG 格式');
    }
  } else {
    // 创建最小 PNG
    imageBuffer = createMinimalPNG();
  }

  // 嵌入角色卡数据
  const outputBuffer = embedCharaInPNG(imageBuffer, normalized);

  // 保存文件
  fs.writeFileSync(outputPath, outputBuffer);

  return {
    path: outputPath,
    size: outputBuffer.length,
    format: 'png',
    spec: normalized.spec
  };
}

/**
 * 主函数：导出角色卡为 JSON
 */
async function exportCharacterCardJSON(characterData, outputPath) {
  // 规范化数据
  const normalized = normalizeCharacterCard(characterData);

  // 验证数据
  const validation = validateCharacterCard(normalized);
  if (!validation.valid) {
    throw new Error(`角色卡数据验证失败:\n${validation.errors.join('\n')}`);
  }

  // 保存文件
  const jsonStr = JSON.stringify(normalized, null, 2);
  fs.writeFileSync(outputPath, jsonStr, 'utf8');

  return {
    path: outputPath,
    size: jsonStr.length,
    format: 'json',
    spec: normalized.spec
  };
}

module.exports = {
  detectFileFormat,
  extractCharaFromPNG,
  normalizeCharacterCard,
  upgradeToV3,
  validateCharacterCard,
  formatCharacterInfo,
  embedCharaInPNG,
  createMinimalPNG,
  importCharacterCard,
  exportCharacterCardPNG,
  exportCharacterCardJSON
};
