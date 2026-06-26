/**
 * 设计比对验证模块
 * 将实际实现（CSS/代码）与Figma设计进行比对
 */

const fs = require('fs');
const path = require('path');
const { extractDesignSystem } = require('./design-extractor');

/**
 * 解析CSS文件，提取样式规则
 * @param {string} cssFilePath - CSS文件路径
 * @returns {Promise<object>} 解析的CSS规则
 */
async function parseCSS(cssFilePath) {
  try {
    const cssContent = fs.readFileSync(cssFilePath, 'utf8');
    const rules = {
      colors: [],
      fonts: [],
      spacing: [],
      border_radius: [],
      shadows: [],
      selectors: []
    };

    // 简单的CSS解析（实际项目中可能需要更复杂的解析器）
    const lines = cssContent.split('\n');
    let currentSelector = '';
    let inComment = false;

    for (const line of lines) {
      const trimmed = line.trim();

      // 处理多行注释
      if (trimmed.includes('/*')) {
        inComment = true;
      }
      if (trimmed.includes('*/')) {
        inComment = false;
        continue;
      }
      if (inComment) {
        continue;
      }

      // 提取选择器
      if (trimmed.endsWith('{') && !trimmed.includes('@')) {
        currentSelector = trimmed.slice(0, -1).trim();
        rules.selectors.push({
          selector: currentSelector,
          properties: []
        });
        continue;
      }

      // 提取属性
      if (currentSelector && trimmed.includes(':')) {
        const [property, ...valueParts] = trimmed.split(':');
        const value = valueParts.join(':').replace(';', '').trim();

        // 记录属性
        const lastSelector = rules.selectors[rules.selectors.length - 1];
        if (lastSelector) {
          lastSelector.properties.push({ property, value });
        }

        // 提取颜色
        const colorMatch = extractColorFromValue(value);
        if (colorMatch) {
          rules.colors.push({
            selector: currentSelector,
            property: property,
            value: value,
            color: colorMatch
          });
        }

        // 提取字体
        if (property.includes('font')) {
          rules.fonts.push({
            selector: currentSelector,
            property: property,
            value: value
          });
        }

        // 提取间距
        if (property.includes('margin') || property.includes('padding') ||
            property.includes('gap') || property.includes('width') ||
            property.includes('height') || property.includes('top') ||
            property.includes('right') || property.includes('bottom') ||
            property.includes('left')) {
          const spacingMatch = extractSpacingFromValue(value);
          if (spacingMatch) {
            rules.spacing.push({
              selector: currentSelector,
              property: property,
              value: value,
              spacing: spacingMatch
            });
          }
        }

        // 提取圆角
        if (property.includes('radius')) {
          const radiusMatch = extractRadiusFromValue(value);
          if (radiusMatch) {
            rules.border_radius.push({
              selector: currentSelector,
              property: property,
              value: value,
              radius: radiusMatch
            });
          }
        }

        // 提取阴影
        if (property.includes('shadow')) {
          const shadowMatch = extractShadowFromValue(value);
          if (shadowMatch) {
            rules.shadows.push({
              selector: currentSelector,
              property: property,
              value: value,
              shadow: shadowMatch
            });
          }
        }
      }

      // 结束选择器
      if (trimmed.includes('}')) {
        currentSelector = '';
      }
    }

    return rules;

  } catch (error) {
    console.error('解析CSS文件失败:', error.message);
    throw error;
  }
}

/**
 * 从值中提取颜色
 */
function extractColorFromValue(value) {
  // HEX颜色
  const hexMatch = value.match(/#([0-9A-Fa-f]{3,8})/);
  if (hexMatch) {
    return {
      type: 'hex',
      value: hexMatch[0],
      original: value
    };
  }

  // RGB/RGBA颜色
  const rgbMatch = value.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)/i);
  if (rgbMatch) {
    return {
      type: rgbMatch[0].startsWith('rgba') ? 'rgba' : 'rgb',
      value: rgbMatch[0],
      r: parseInt(rgbMatch[1]),
      g: parseInt(rgbMatch[2]),
      b: parseInt(rgbMatch[3]),
      original: value
    };
  }

  // 颜色名称
  const colorNames = [
    'red', 'green', 'blue', 'black', 'white', 'gray', 'grey',
    'yellow', 'purple', 'orange', 'pink', 'brown', 'cyan', 'magenta'
  ];
  const lowerValue = value.toLowerCase();
  if (colorNames.includes(lowerValue)) {
    return {
      type: 'named',
      value: lowerValue,
      original: value
    };
  }

  return null;
}

/**
 * 从值中提取间距
 */
function extractSpacingFromValue(value) {
  // 匹配数字和单位
  const match = value.match(/([\d.]+)(px|rem|em|%)?/);
  if (match) {
    return {
      value: parseFloat(match[1]),
      unit: match[2] || 'px',
      original: value
    };
  }
  return null;
}

/**
 * 从值中提取圆角
 */
function extractRadiusFromValue(value) {
  const match = value.match(/([\d.]+)(px|rem|em|%)?/);
  if (match) {
    return {
      value: parseFloat(match[1]),
      unit: match[2] || 'px',
      original: value
    };
  }
  return null;
}

/**
 * 从值中提取阴影
 */
function extractShadowFromValue(value) {
  // 简单的阴影解析
  const parts = value.split(/\s+/);
  if (parts.length >= 3) {
    return {
      offsetX: parts[0],
      offsetY: parts[1],
      blur: parts[2],
      color: parts[3] || 'rgba(0,0,0,0.5)',
      original: value
    };
  }
  return null;
}

/**
 * 比对Figma设计与CSS实现
 * @param {string} fileId - Figma文件ID
 * @param {string} implementationPath - 实现文件路径
 * @param {string} token - Figma个人访问令牌
 * @returns {Promise<object>} 比对结果
 */
async function compareWithImplementation(fileId, implementationPath, token) {
  try {
    console.log('开始比对验证...');

    // 1. 提取Figma设计系统
    console.log('提取Figma设计系统...');
    const figmaDesign = await extractDesignSystem(fileId, token);

    // 2. 解析实现文件
    console.log('解析实现文件...');
    const fileExt = path.extname(implementationPath).toLowerCase();
    let implementation;

    if (fileExt === '.css') {
      implementation = await parseCSS(implementationPath);
    } else {
      // 支持其他文件类型的扩展
      implementation = await parseGenericFile(implementationPath);
    }

    // 3. 进行比对
    console.log('进行比对分析...');
    const comparison = compareDesignSystems(figmaDesign, implementation);

    // 4. 生成报告
    const report = {
      file_id: fileId,
      implementation_file: implementationPath,
      comparison_time: new Date().toISOString(),
      summary: {
        total_checks: comparison.total_checks,
        passed: comparison.passed,
        failed: comparison.failed,
        pass_rate: Math.round((comparison.passed / comparison.total_checks) * 100)
      },
      details: comparison.details,
      recommendations: generateRecommendations(comparison)
    };

    // 5. 生成HTML报告（如果需要）
    const htmlReport = generateHTMLReport(report);

    return {
      json_report: report,
      html_report: htmlReport,
      figma_design_summary: {
        total_colors: figmaDesign.summary.total_colors,
        total_fonts: figmaDesign.summary.total_fonts,
        total_components: figmaDesign.summary.total_components
      },
      implementation_summary: {
        total_colors: implementation.colors.length,
        total_fonts: implementation.fonts.length,
        total_selectors: implementation.selectors.length
      }
    };

  } catch (error) {
    console.error('比对验证失败:', error.message);
    throw error;
  }
}

/**
 * 解析通用文件类型
 */
async function parseGenericFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');

  // 简单分析，提取可能的设计相关值
  return {
    colors: extractColorsFromText(content),
    fonts: extractFontsFromText(content),
    spacing: extractSpacingFromText(content),
    content_preview: content.substring(0, 500) + '...'
  };
}

/**
 * 从文本中提取颜色
 */
function extractColorsFromText(text) {
  const colors = [];

  // HEX颜色
  const hexRegex = /#([0-9A-Fa-f]{3,8})/g;
  let match;
  while ((match = hexRegex.exec(text)) !== null) {
    colors.push({
      type: 'hex',
      value: match[0],
      position: match.index
    });
  }

  // RGB颜色
  const rgbRegex = /rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)/gi;
  while ((match = rgbRegex.exec(text)) !== null) {
    colors.push({
      type: match[0].startsWith('rgba') ? 'rgba' : 'rgb',
      value: match[0],
      position: match.index
    });
  }

  return colors;
}

/**
 * 从文本中提取字体
 */
function extractFontsFromText(text) {
  const fonts = [];

  // 简单的字体匹配
  const fontRegex = /font-(?:family|size|weight):\s*([^;]+)/gi;
  let match;
  while ((match = fontRegex.exec(text)) !== null) {
    fonts.push({
      property: match[0].split(':')[0].trim(),
      value: match[1].trim()
    });
  }

  return fonts;
}

/**
 * 从文本中提取间距
 */
function extractSpacingFromText(text) {
  const spacing = [];

  // 匹配数字加单位
  const spacingRegex = /(\d+(?:\.\d+)?)(px|rem|em|%)/g;
  let match;
  while ((match = spacingRegex.exec(text)) !== null) {
    spacing.push({
      value: parseFloat(match[1]),
      unit: match[2],
      position: match.index
    });
  }

  return spacing;
}

/**
 * 比对两个设计系统
 */
function compareDesignSystems(figmaDesign, implementation) {
  const comparison = {
    total_checks: 0,
    passed: 0,
    failed: 0,
    details: {
      colors: [],
      fonts: [],
      spacing: [],
      components: []
    }
  };

  // 比对颜色
  if (figmaDesign.colors && implementation.colors) {
    figmaDesign.colors.forEach(figmaColor => {
      const matched = implementation.colors.some(implColor =>
        colorsMatch(figmaColor, implColor)
      );

      comparison.details.colors.push({
        figma_color: figmaColor.hex,
        matched: matched,
        figma_source: figmaColor.source,
        implementation_match: matched ? '找到匹配' : '未找到匹配'
      });

      comparison.total_checks++;
      if (matched) comparison.passed++; else comparison.failed++;
    });
  }

  // 比对字体
  if (figmaDesign.fonts && implementation.fonts) {
    figmaDesign.fonts.forEach(figmaFont => {
      const matched = implementation.fonts.some(implFont =>
        fontsMatch(figmaFont, implFont)
      );

      comparison.details.fonts.push({
        figma_font: `${figmaFont.font_family} ${figmaFont.font_size}px`,
        matched: matched,
        figma_source: figmaFont.source
      });

      comparison.total_checks++;
      if (matched) comparison.passed++; else comparison.failed++;
    });
  }

  // 比对间距
  if (figmaDesign.spacing && implementation.spacing) {
    figmaDesign.spacing.forEach(figmaSpacing => {
      const matched = implementation.spacing.some(implSpacing =>
        spacingMatch(figmaSpacing, implSpacing)
      );

      comparison.details.spacing.push({
        figma_spacing: `${figmaSpacing.value}${figmaSpacing.unit}`,
        matched: matched,
        figma_source: figmaSpacing.source
      });

      comparison.total_checks++;
      if (matched) comparison.passed++; else comparison.failed++;
    });
  }

  return comparison;
}

/**
 * 检查颜色是否匹配
 */
function colorsMatch(figmaColor, implColor) {
  if (!implColor.color) return false;

  if (implColor.color.type === 'hex') {
    return implColor.color.value.toLowerCase() === figmaColor.hex.toLowerCase();
  }

  if (implColor.color.type === 'rgb' || implColor.color.type === 'rgba') {
    // 简单的RGB比较
    const figmaRGB = `rgb(${figmaColor.r}, ${figmaColor.g}, ${figmaColor.b})`;
    return implColor.color.value.includes(figmaRGB);
  }

  return false;
}

/**
 * 检查字体是否匹配
 */
function fontsMatch(figmaFont, implFont) {
  // 简单的字体大小匹配
  if (implFont.value && figmaFont.font_size) {
    const sizeMatch = implFont.value.includes(`${figmaFont.font_size}px`);
    return sizeMatch;
  }
  return false;
}

/**
 * 检查间距是否匹配
 */
function spacingMatch(figmaSpacing, implSpacing) {
  if (!implSpacing.spacing) return false;

  // 允许一定的误差
  const tolerance = 1;
  const difference = Math.abs(figmaSpacing.value - implSpacing.spacing.value);

  return difference <= tolerance && implSpacing.spacing.unit === figmaSpacing.unit;
}

/**
 * 生成改进建议
 */
function generateRecommendations(comparison) {
  const recommendations = [];

  if (comparison.failed > 0) {
    const failRate = (comparison.failed / comparison.total_checks) * 100;

    if (failRate > 50) {
      recommendations.push({
        priority: 'high',
        message: '设计一致性较低，建议全面检查设计实现',
        action: '重新审查Figma设计规范并与开发团队对齐'
      });
    } else if (failRate > 20) {
      recommendations.push({
        priority: 'medium',
        message: '存在多个不一致的设计元素',
        action: '优先修复颜色和字体等关键设计元素'
      });
    } else {
      recommendations.push({
        priority: 'low',
        message: '基本一致，只有少量不一致',
        action: '修复个别不一致的设计元素'
      });
    }

    // 具体建议
    if (comparison.details.colors.filter(c => !c.matched).length > 0) {
      recommendations.push({
        priority: 'medium',
        message: '颜色不一致',
        action: '检查并更新CSS中的颜色值以匹配Figma设计'
      });
    }

    if (comparison.details.fonts.filter(f => !f.matched).length > 0) {
      recommendations.push({
        priority: 'medium',
        message: '字体不一致',
        action: '检查字体大小、字重和行高设置'
      });
    }
  } else {
    recommendations.push({
      priority: 'low',
      message: '完美匹配！设计实现与Figma设计完全一致',
      action: '继续保持良好的设计开发协作流程'
    });
  }

  return recommendations;
}

/**
 * 生成HTML报告
 */
function generateHTMLReport(report) {
  const html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma设计比对报告</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .summary-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .pass-rate {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin: 1rem 0;
        }
        .pass { color: #10b981; }
        .fail { color: #ef4444; }
        .warning { color: #f59e0b; }
        .details-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        .details-table th,
        .details-table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        .details-table th {
            background-color: #f9fafb;
            font-weight: 600;
        }
        .recommendation {
            background: #f0f9ff;
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        .priority-high { border-left-color: #ef4444; background: #fef2f2; }
        .priority-medium { border-left-color: #f59e0b; background: #fffbeb; }
        .priority-low { border-left-color: #10b981; background: #f0fdf4; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 Figma设计比对报告</h1>
        <p>文件ID: ${report.file_id} | 比对时间: ${new Date(report.comparison_time).toLocaleString()}</p>
    </div>

    <div class="summary-card">
        <h2>📊 比对摘要</h2>
        <div class="pass-rate ${report.summary.pass_rate >= 80 ? 'pass' : report.summary.pass_rate >= 60 ? 'warning' : 'fail'}">
            ${report.summary.pass_rate}% 通过率
        </div>
        <p>总计检查: ${report.summary.total_checks} | 通过: ${report.summary.passed} | 失败: ${report.summary.failed}</p>
    </div>

    <div class="summary-card">
        <h2>🔍 详细比对结果</h2>

        <h3>颜色比对</h3>
        <table class="details-table">
            <thead>
                <tr>
                    <th>Figma颜色</th>
                    <th>匹配状态</th>
                    <th>说明</th>
                </tr>
            </thead>
            <tbody>
                ${report.details.colors.map(color => `
                <tr>
                    <td><span style="display: inline-block; width: 20px; height: 20px; background-color: ${color.figma_color}; border: 1px solid #ccc; margin-right: 8px;"></span>${color.figma_color}</td>
                    <td>${color.matched ? '✅ 匹配' : '❌ 不匹配'}</td>
                    <td>${color.implementation_match}</td>
                </tr>
                `).join('')}
            </tbody>
        </table>

        <h3>字体比对</h3>
        <table class="details-table">
            <thead>
                <tr>
                    <th>Figma字体</th>
                    <th>匹配状态</th>
                </tr>
            </thead>
            <tbody>
                ${report.details.fonts.map(font => `
                <tr>
                    <td>${font.figma_font}</td>
                    <td>${font.matched ? '✅ 匹配' : '❌ 不匹配'}</td>
                </tr>
                `).join('')}
            </tbody>
        </table>
    </div>

    <div class="summary-card">
        <h2>💡 改进建议</h2>
        ${report.recommendations.map(rec => `
        <div class="recommendation priority-${rec.priority}">
            <strong>${rec.priority === 'high' ? '🔴 高优先级' : rec.priority === 'medium' ? '🟡 中优先级' : '🟢 低优先级'}</strong>
            <p>${rec.message}</p>
            <p><em>建议操作: ${rec.action}</em></p>
        </div>
        `).join('')}
    </div>

    <div class="summary-card">
        <h2>📈 数据统计</h2>
        <p>Figma设计系统: ${report.figma_design_summary.total_colors}种颜色, ${report.figma_design_summary.total_fonts}种字体, ${report.figma_design_summary.total_components}个组件</p>
        <p>实现文件: ${report.implementation_summary.total_colors}种颜色, ${report.implementation_summary.total_fonts}种字体, ${report.implementation_summary.total_selectors}个选择器</p>
    </div>
</body>
</html>
  `;

  return html;
}

module.exports = {
  compareWithImplementation,
  parseCSS,
  generateHTMLReport
};