/**
 * yaml-lite.js - 轻量 YAML 解析器
 * 
 * 零外部依赖，仅支持 SKILL.md frontmatter 常用的简单 YAML 格式：
 * - key: value（字符串、数字、布尔）
 * - key: [a, b, c]（内联数组）
 * - 多行字符串（> 折叠）
 * 
 * 不支持：嵌套对象、锚点、复杂类型
 * 如需完整 YAML，请安装 js-yaml
 */

function parse(text) {
  if (!text || typeof text !== 'string') return {};

  const result = {};
  const lines = text.split(/\r?\n/);
  let currentKey = null;
  let multilineValue = '';
  let isMultiline = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // 跳过注释和空行（非多行模式）
    if (!isMultiline && (line.trim().startsWith('#') || line.trim() === '')) continue;

    // 多行值收集
    if (isMultiline) {
      if (line.match(/^\S/) && line.includes(':')) {
        // 新的 key 开始，结束多行
        result[currentKey] = multilineValue.trim();
        isMultiline = false;
        // 继续解析当前行
      } else {
        multilineValue += ' ' + line.trim();
        continue;
      }
    }

    // key: value 解析
    const kvMatch = line.match(/^(\w[\w\s.-]*?):\s*(.*)/);
    if (!kvMatch) continue;

    const key = kvMatch[1].trim();
    let value = kvMatch[2].trim();

    // 多行标记 (> 或 |)
    if (value === '>' || value === '|') {
      currentKey = key;
      multilineValue = '';
      isMultiline = true;
      continue;
    }

    // 内联数组 [a, b, c]
    if (value.startsWith('[') && value.endsWith(']')) {
      const inner = value.slice(1, -1);
      result[key] = inner.split(',').map(s => parseValue(s.trim()));
      continue;
    }

    // 空数组标记 []
    if (value === '[]') {
      result[key] = [];
      continue;
    }

    // 去除行内注释
    const commentIdx = value.indexOf(' #');
    if (commentIdx > 0) {
      value = value.slice(0, commentIdx).trim();
    }

    result[key] = parseValue(value);
  }

  // 处理最后一个多行值
  if (isMultiline && currentKey) {
    result[currentKey] = multilineValue.trim();
  }

  return result;
}

function parseValue(value) {
  if (value === '') return '';

  // 去引号
  if ((value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }

  // 布尔
  if (value === 'true') return true;
  if (value === 'false') return false;

  // null
  if (value === 'null' || value === '~') return null;

  // 数字
  if (/^-?\d+(\.\d+)?$/.test(value)) return Number(value);

  return value;
}

function stringify(obj) {
  if (!obj || typeof obj !== 'object') return '';

  const lines = [];
  for (const [key, value] of Object.entries(obj)) {
    if (Array.isArray(value)) {
      if (value.length === 0) {
        lines.push(`${key}: []`);
      } else {
        lines.push(`${key}: [${value.map(v => JSON.stringify(v)).join(', ')}]`);
      }
    } else if (typeof value === 'string' && value.includes('\n')) {
      lines.push(`${key}: >`);
      lines.push(`  ${value.replace(/\n/g, '\n  ')}`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  return lines.join('\n');
}

module.exports = { parse, stringify };
