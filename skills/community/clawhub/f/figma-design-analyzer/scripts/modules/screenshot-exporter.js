/**
 * 截图导出模块
 * 导出Figma设计节点的PNG/JPG截图
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

/**
 * 导出Figma节点截图
 * @param {string} fileId - Figma文件ID
 * @param {string} nodeId - 节点ID
 * @param {string} token - Figma个人访问令牌
 * @param {string} format - 图片格式 (png, jpg)
 * @param {number} scale - 缩放比例
 * @returns {Promise<object>} 截图结果
 */
async function exportScreenshot(fileId, nodeId, token, format = 'png', scale = 1) {
  try {
    const headers = {
      'X-Figma-Token': token
    };

    console.log(`请求截图: file=${fileId}, node=${nodeId}, scale=${scale}, format=${format}`);

    // 1. 获取截图URL
    const imageResponse = await axios.get(
      `https://api.figma.com/v1/images/${fileId}?ids=${nodeId}&scale=${scale}&format=${format}`,
      { headers }
    );

    const imageData = imageResponse.data;
    const imageUrl = imageData.images[nodeId];

    if (!imageUrl) {
      throw new Error(`未找到节点 ${nodeId} 的截图URL`);
    }

    // 2. 下载图片
    console.log(`下载截图: ${imageUrl}`);
    const imageResponse2 = await axios.get(imageUrl, {
      responseType: 'arraybuffer'
    });

    const imageBuffer = Buffer.from(imageResponse2.data, 'binary');

    // 3. 保存图片
    const outputDir = path.join(process.cwd(), 'figma-exports', 'screenshots');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `figma-${fileId}-${nodeId}-${scale}x-${timestamp}.${format}`;
    const outputPath = path.join(outputDir, filename);

    // 4. 处理图片（如果需要）
    let finalBuffer = imageBuffer;
    if (format === 'jpg' || format === 'jpeg') {
      // 转换PNG到JPG
      finalBuffer = await sharp(imageBuffer)
        .jpeg({ quality: 90 })
        .toBuffer();
    }

    // 5. 保存文件
    fs.writeFileSync(outputPath, finalBuffer);
    console.log(`截图已保存: ${outputPath}`);

    // 6. 获取节点信息以提供更多上下文
    let nodeInfo = null;
    try {
      const nodeResponse = await axios.get(
        `https://api.figma.com/v1/files/${fileId}/nodes?ids=${nodeId}`,
        { headers }
      );
      nodeInfo = nodeResponse.data.nodes[nodeId];
    } catch (error) {
      console.warn('无法获取节点信息:', error.message);
    }

    // 返回结果
    const result = {
      success: true,
      file_id: fileId,
      node_id: nodeId,
      image_path: outputPath,
      image_url: imageUrl,
      format: format,
      scale: scale,
      dimensions: await getImageDimensions(finalBuffer),
      node_info: nodeInfo ? {
        name: nodeInfo.document?.name,
        type: nodeInfo.document?.type,
        bounds: nodeInfo.document?.absoluteBoundingBox
      } : null,
      export_time: new Date().toISOString()
    };

    return result;

  } catch (error) {
    console.error('导出截图失败:', error.message);

    if (error.response) {
      const status = error.response.status;
      const errorData = error.response.data;

      switch (status) {
        case 400:
          throw new Error(`无效请求: ${errorData?.message || '请检查节点ID和文件ID'}`);
        case 404:
          throw new Error(`节点不存在: ${nodeId}`);
        case 429:
          throw new Error('API限制: 已达到截图导出限制，请稍后重试');
        default:
          throw new Error(`Figma API错误 (${status}): ${errorData?.message || '未知错误'}`);
      }
    } else if (error.request) {
      throw new Error('网络错误: 无法连接到Figma API');
    } else {
      throw new Error(`截图处理错误: ${error.message}`);
    }
  }
}

/**
 * 获取图片尺寸
 */
async function getImageDimensions(buffer) {
  try {
    const metadata = await sharp(buffer).metadata();
    return {
      width: metadata.width,
      height: metadata.height,
      size_bytes: buffer.length,
      format: metadata.format
    };
  } catch (error) {
    console.warn('无法获取图片尺寸:', error.message);
    return { width: 0, height: 0, size_bytes: buffer.length };
  }
}

/**
 * 批量导出多个节点截图
 * @param {string} fileId - Figma文件ID
 * @param {string[]} nodeIds - 节点ID数组
 * @param {string} token - Figma个人访问令牌
 * @param {string} format - 图片格式
 * @param {number} scale - 缩放比例
 * @returns {Promise<object[]>} 截图结果数组
 */
async function exportMultipleScreenshots(fileId, nodeIds, token, format = 'png', scale = 1) {
  try {
    const headers = {
      'X-Figma-Token': token
    };

    const idsParam = nodeIds.join(',');
    console.log(`批量导出截图: ${nodeIds.length}个节点`);

    // 1. 获取所有截图URL
    const imageResponse = await axios.get(
      `https://api.figma.com/v1/images/${fileId}?ids=${idsParam}&scale=${scale}&format=${format}`,
      { headers }
    );

    const imageData = imageResponse.data;
    const results = [];

    // 2. 批量下载和保存
    for (const nodeId of nodeIds) {
      const imageUrl = imageData.images[nodeId];
      if (!imageUrl) {
        console.warn(`节点 ${nodeId} 没有截图URL，跳过`);
        continue;
      }

      try {
        console.log(`处理节点 ${nodeId}...`);
        const imageResponse2 = await axios.get(imageUrl, {
          responseType: 'arraybuffer'
        });

        const imageBuffer = Buffer.from(imageResponse2.data, 'binary');

        // 创建输出目录
        const outputDir = path.join(process.cwd(), 'figma-exports', 'batch-screenshots');
        if (!fs.existsSync(outputDir)) {
          fs.mkdirSync(outputDir, { recursive: true });
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `figma-${fileId}-${nodeId}-${scale}x-${timestamp}.${format}`;
        const outputPath = path.join(outputDir, filename);

        // 处理图片格式
        let finalBuffer = imageBuffer;
        if (format === 'jpg' || format === 'jpeg') {
          finalBuffer = await sharp(imageBuffer)
            .jpeg({ quality: 90 })
            .toBuffer();
        }

        // 保存文件
        fs.writeFileSync(outputPath, finalBuffer);

        results.push({
          node_id: nodeId,
          image_path: outputPath,
          success: true,
          error: null
        });

        console.log(`✓ 已保存: ${filename}`);

      } catch (error) {
        console.error(`处理节点 ${nodeId} 失败:`, error.message);
        results.push({
          node_id: nodeId,
          image_path: null,
          success: false,
          error: error.message
        });
      }
    }

    // 3. 生成汇总报告
    const summary = {
      total_nodes: nodeIds.length,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      file_id: fileId,
      format: format,
      scale: scale,
      export_time: new Date().toISOString()
    };

    // 保存汇总报告
    const reportDir = path.join(process.cwd(), 'figma-exports', 'reports');
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }

    const reportPath = path.join(reportDir, `batch-export-${Date.now()}.json`);
    const reportData = {
      summary: summary,
      details: results
    };

    fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2));
    console.log(`批量导出报告已保存: ${reportPath}`);

    return reportData;

  } catch (error) {
    console.error('批量导出失败:', error.message);
    throw error;
  }
}

/**
 * 导出整个画板或页面
 * @param {string} fileId - Figma文件ID
 * @param {string} pageId - 页面ID
 * @param {string} token - Figma个人访问令牌
 * @param {string} format - 图片格式
 * @param {number} scale - 缩放比例
 * @returns {Promise<object>} 导出结果
 */
async function exportPage(fileId, pageId, token, format = 'png', scale = 1) {
  try {
    // 首先获取页面中的所有节点
    const headers = {
      'X-Figma-Token': token
    };

    // 获取页面信息
    const nodesResponse = await axios.get(
      `https://api.figma.com/v1/files/${fileId}/nodes?ids=${pageId}`,
      { headers }
    );

    const pageData = nodesResponse.data.nodes[pageId];
    if (!pageData) {
      throw new Error(`页面 ${pageId} 不存在`);
    }

    // 提取页面中的所有节点ID
    const nodeIds = extractAllNodeIds(pageData.document);
    console.log(`页面包含 ${nodeIds.length} 个节点`);

    // 批量导出所有节点
    return await exportMultipleScreenshots(fileId, nodeIds, token, format, scale);

  } catch (error) {
    console.error('导出页面失败:', error.message);
    throw error;
  }
}

/**
 * 递归提取所有节点ID
 */
function extractAllNodeIds(node, ids = []) {
  if (!node) return ids;

  ids.push(node.id);

  if (node.children && Array.isArray(node.children)) {
    node.children.forEach(child => {
      extractAllNodeIds(child, ids);
    });
  }

  return ids;
}

module.exports = {
  exportScreenshot,
  exportMultipleScreenshots,
  exportPage
};