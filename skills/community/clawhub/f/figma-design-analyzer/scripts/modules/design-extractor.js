/**
 * 设计系统提取模块
 * 提取颜色、字体、间距、组件等设计属性
 */

const axios = require('axios');

/**
 * 递归遍历节点，提取设计属性
 * @param {object} node - Figma节点
 * @param {object} result - 结果对象
 */
function traverseNode(node, result) {
  if (!node) return;

  // 提取颜色
  if (node.fills && Array.isArray(node.fills)) {
    node.fills.forEach(fill => {
      if (fill.type === 'SOLID' && fill.color) {
        const color = {
          r: Math.round(fill.color.r * 255),
          g: Math.round(fill.color.g * 255),
          b: Math.round(fill.color.b * 255),
          a: fill.color.a || 1
        };
        const hex = rgbToHex(color.r, color.g, color.b);
        const rgba = `rgba(${color.r}, ${color.g}, ${color.b}, ${color.a})`;

        // 检查是否已存在相同颜色
        const existingColor = result.colors.find(c => c.hex === hex && c.a === color.a);
        if (!existingColor) {
          result.colors.push({
            hex: hex,
            rgba: rgba,
            r: color.r,
            g: color.g,
            b: color.b,
            a: color.a,
            source: `node:${node.id}`,
            type: 'fill'
          });
        }
      }
    });
  }

  // 提取描边颜色
  if (node.strokes && Array.isArray(node.strokes)) {
    node.strokes.forEach(stroke => {
      if (stroke.type === 'SOLID' && stroke.color) {
        const color = {
          r: Math.round(stroke.color.r * 255),
          g: Math.round(stroke.color.g * 255),
          b: Math.round(stroke.color.b * 255),
          a: stroke.color.a || 1
        };
        const hex = rgbToHex(color.r, color.g, color.b);
        const rgba = `rgba(${color.r}, ${color.g}, ${color.b}, ${color.a})`;

        const existingColor = result.colors.find(c => c.hex === hex && c.a === color.a);
        if (!existingColor) {
          result.colors.push({
            hex: hex,
            rgba: rgba,
            r: color.r,
            g: color.g,
            b: color.b,
            a: color.a,
            source: `node:${node.id}`,
            type: 'stroke'
          });
        }
      }
    });
  }

  // 提取字体
  if (node.style) {
    const style = node.style;

    if (style.fontFamily || style.fontSize || style.fontWeight) {
      const fontKey = `${style.fontFamily}-${style.fontSize}-${style.fontWeight}-${style.lineHeightPx}`;

      if (!result.fonts.some(f => f.key === fontKey)) {
        result.fonts.push({
          font_family: style.fontFamily,
          font_size: style.fontSize,
          font_weight: style.fontWeight,
          line_height_px: style.lineHeightPx,
          line_height_percent: style.lineHeightPercent,
          letter_spacing: style.letterSpacing,
          text_case: style.textCase,
          text_decoration: style.textDecoration,
          key: fontKey,
          source: `node:${node.id}`,
          text_style: node.name // 可能包含"H1"、"Body"等样式名称
        });
      }
    }
  }

  // 提取间距和尺寸
  if (node.absoluteBoundingBox) {
    const bounds = node.absoluteBoundingBox;
    const width = bounds.width;
    const height = bounds.height;

    if (width > 0 && !result.spacing.some(s => s.value === width && s.type === 'width')) {
      result.spacing.push({
        value: Math.round(width),
        type: 'width',
        source: `node:${node.id}`,
        unit: 'px'
      });
    }

    if (height > 0 && !result.spacing.some(s => s.value === height && s.type === 'height')) {
      result.spacing.push({
        value: Math.round(height),
        type: 'height',
        source: `node:${node.id}`,
        unit: 'px'
      });
    }
  }

  // 提取圆角
  if (node.cornerRadius !== undefined && node.cornerRadius > 0) {
    const radius = node.cornerRadius;
    if (!result.border_radius.some(r => r.value === radius)) {
      result.border_radius.push({
        value: radius,
        source: `node:${node.id}`,
        unit: 'px'
      });
    }
  }

  // 提取阴影
  if (node.effects && Array.isArray(node.effects)) {
    node.effects.forEach(effect => {
      if (effect.type === 'DROP_SHADOW' || effect.type === 'INNER_SHADOW') {
        const shadowKey = `${effect.type}-${effect.radius}-${effect.offset.x}-${effect.offset.y}`;

        if (!result.shadows.some(s => s.key === shadowKey)) {
          result.shadows.push({
            type: effect.type,
            radius: effect.radius,
            offset: {
              x: effect.offset.x,
              y: effect.offset.y
            },
            color: effect.color ? {
              r: Math.round(effect.color.r * 255),
              g: Math.round(effect.color.g * 255),
              b: Math.round(effect.color.b * 255),
              a: effect.color.a || 1,
              hex: rgbToHex(
                Math.round(effect.color.r * 255),
                Math.round(effect.color.g * 255),
                Math.round(effect.color.b * 255)
              )
            } : null,
            key: shadowKey,
            source: `node:${node.id}`
          });
        }
      }
    });
  }

  // 递归处理子节点
  if (node.children && Array.isArray(node.children)) {
    node.children.forEach(child => {
      traverseNode(child, result);
    });
  }
}

/**
 * RGB转十六进制
 */
function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

/**
 * 从Figma文件中提取设计系统
 * @param {string} fileId - Figma文件ID
 * @param {string} token - Figma个人访问令牌
 * @returns {Promise<object>} 设计系统数据
 */
async function extractDesignSystem(fileId, token) {
  try {
    const headers = {
      'X-Figma-Token': token
    };

    // 获取完整的文件数据
    const response = await axios.get(`https://api.figma.com/v1/files/${fileId}`, { headers });
    const fileData = response.data;

    // 初始化结果对象
    const result = {
      file_id: fileId,
      file_name: fileData.name,
      extracted_at: new Date().toISOString(),
      summary: {
        total_pages: fileData.document?.children?.length || 0,
        total_components: fileData.components ? Object.keys(fileData.components).length : 0,
        total_styles: fileData.styles ? Object.keys(fileData.styles).length : 0
      },
      colors: [],
      fonts: [],
      spacing: [],
      border_radius: [],
      shadows: [],
      components: [],
      design_tokens: {}
    };

    // 提取颜色样式
    if (fileData.styles) {
      Object.entries(fileData.styles).forEach(([styleId, styleInfo]) => {
        if (styleInfo.styleType === 'FILL') {
          // 颜色样式
          result.design_tokens[styleInfo.name] = {
            type: 'color',
            style_id: styleId,
            description: styleInfo.description || ''
          };
        } else if (styleInfo.styleType === 'TEXT') {
          // 文本样式
          result.design_tokens[styleInfo.name] = {
            type: 'text',
            style_id: styleId,
            description: styleInfo.description || ''
          };
        }
      });
    }

    // 提取组件信息
    if (fileData.components) {
      Object.entries(fileData.components).forEach(([componentId, componentInfo]) => {
        result.components.push({
          id: componentId,
          name: componentInfo.name,
          key: componentInfo.key,
          description: componentInfo.description || '',
          documentation_links: componentInfo.documentationLinks || []
        });
      });
    }

    // 遍历所有页面和节点，提取设计属性
    if (fileData.document?.children) {
      fileData.document.children.forEach(page => {
        traverseNode(page, result);
      });
    }

    // 对结果进行排序和去重
    result.colors.sort((a, b) => a.hex.localeCompare(b.hex));
    result.fonts.sort((a, b) => a.font_size - b.font_size);
    result.spacing.sort((a, b) => a.value - b.value);
    result.border_radius.sort((a, b) => a.value - b.value);

    // 统计信息
    result.summary.total_colors = result.colors.length;
    result.summary.total_fonts = result.fonts.length;
    result.summary.total_spacing_values = result.spacing.length;
    result.summary.total_border_radius = result.border_radius.length;
    result.summary.total_shadows = result.shadows.length;

    // 计算常见值
    result.analysis = {
      most_common_colors: findMostCommonValues(result.colors, 'hex', 5),
      font_sizes_used: [...new Set(result.fonts.map(f => f.font_size))].sort((a, b) => a - b),
      spacing_scale: extractSpacingScale(result.spacing),
      color_categories: categorizeColors(result.colors)
    };

    return result;

  } catch (error) {
    console.error('提取设计系统失败:', error.message);
    throw error;
  }
}

/**
 * 找出最常见的值
 */
function findMostCommonValues(items, property, count) {
  const frequency = {};
  items.forEach(item => {
    const value = item[property];
    frequency[value] = (frequency[value] || 0) + 1;
  });

  return Object.entries(frequency)
    .sort((a, b) => b[1] - a[1])
    .slice(0, count)
    .map(([value, count]) => ({ value, count }));
}

/**
 * 提取间距尺度
 */
function extractSpacingScale(spacingItems) {
  const values = spacingItems.map(s => s.value);
  const uniqueValues = [...new Set(values)].sort((a, b) => a - b);

  // 尝试找出间距模式（如4px、8px、16px等）
  const scale = [];
  let base = 4; // 常见的基数

  for (let i = 1; i <= 8; i++) {
    const value = base * i;
    if (uniqueValues.includes(value) || Math.abs(value - Math.min(...uniqueValues)) < 2) {
      scale.push({
        multiplier: i,
        value: value,
        used: uniqueValues.includes(value),
        closest_match: findClosestMatch(value, uniqueValues)
      });
    }
  }

  return scale;
}

/**
 * 找到最接近的匹配值
 */
function findClosestMatch(target, values) {
  return values.reduce((prev, curr) => {
    return (Math.abs(curr - target) < Math.abs(prev - target) ? curr : prev);
  });
}

/**
 * 颜色分类
 */
function categorizeColors(colors) {
  const categories = {
    primary: [],
    secondary: [],
    accent: [],
    neutral: [],
    success: [],
    warning: [],
    error: [],
    info: []
  };

  colors.forEach(color => {
    const { r, g, b } = color;

    // 简单分类逻辑
    if (r > 200 && g < 100 && b < 100) {
      categories.primary.push(color);
    } else if (g > 200 && r < 100 && b < 100) {
      categories.success.push(color);
    } else if (r > 200 && g > 150 && b < 100) {
      categories.warning.push(color);
    } else if (r > 200 && g < 100 && b > 200) {
      categories.accent.push(color);
    } else if (Math.abs(r - g) < 30 && Math.abs(g - b) < 30) {
      categories.neutral.push(color);
    } else {
      categories.secondary.push(color);
    }
  });

  // 只保留非空分类
  const result = {};
  Object.entries(categories).forEach(([key, value]) => {
    if (value.length > 0) {
      result[key] = value;
    }
  });

  return result;
}

module.exports = {
  extractDesignSystem
};