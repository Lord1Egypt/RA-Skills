/**
 * 统一配置文件 - 自动根据分辨率适配所有参数
 * 
 * 使用方法：
 * 1. 复制此文件到项目的 scripts/ 目录
 * 2. 确保 scripts/content.json 存在且包含 meta.resolution
 * 3. 在其他脚本中 require('./config')
 */

const fs = require('fs');
const path = require('path');

// 读取 content.json
const contentPath = path.join(__dirname, 'content.json');

if (!fs.existsSync(contentPath)) {
  console.error('❌ 找不到 content.json，请先创建内容脚本');
  process.exit(1);
}

const content = JSON.parse(fs.readFileSync(contentPath, 'utf-8'));

// 验证分辨率配置
if (!content.meta?.resolution?.width || !content.meta?.resolution?.height) {
  console.error('❌ content.json 缺少 meta.resolution 配置');
  console.error('示例：');
  console.error(JSON.stringify({
    meta: {
      resolution: { width: 1080, height: 1920 }
    }
  }, null, 2));
  process.exit(1);
}

const { width, height } = content.meta.resolution;

// 判断方向
const isVertical = height > width;
const isMobile = isVertical; // 竖屏 = 移动端

// 自动计算所有参数
const config = {
  // ========== 基础信息 ==========
  width,
  height,
  isVertical,
  isMobile,
  orientation: isVertical ? 'vertical' : 'horizontal',
  platform: isVertical ? 'mobile' : 'desktop',

  // ========== 字体大小 ==========
  fonts: {
    title: isVertical ? Math.min(width * 0.08, 80) : 48,
    subtitle: isVertical ? Math.min(width * 0.05, 50) : 32,
    body: isVertical ? Math.min(width * 0.04, 40) : 28,
    caption: isVertical ? Math.min(width * 0.035, 35) : 24,
    small: isVertical ? Math.min(width * 0.03, 30) : 20,
  },

  // ========== 间距 ==========
  spacing: {
    lineHeight: isVertical ? 2.6 : 2.4,
    marginBottom: isVertical ? 30 : 20,
    marginTop: isVertical ? 25 : 15,
    paddingHorizontal: isVertical ? width * 0.08 : width * 0.1,
    paddingVertical: isVertical ? height * 0.05 : height * 0.04,
    gap: isVertical ? 20 : 15,
  },

  // ========== 字幕参数（烧录时） ==========
  subtitle: {
    fontSize: isVertical ? 12 : 16,  // 竖屏12px，宽屏16px
    marginV: isVertical ? 20 : 15,   // 竖屏距底部20px，宽屏15px
    maxCharsPerLine: isVertical ? 10 : 20,  // 竖屏每行最多10字，宽屏20字
    fontName: 'Noto Sans CJK SC',
    alignment: 2, // 底部居中
  },

  // ========== 动画参数 ==========
  animation: {
    fadeIn: isVertical ? 10 : 20,      // 竖屏更快
    fadeOut: isVertical ? 8 : 15,
    slideIn: isVertical ? 12 : 20,
    slideDistance: isVertical ? 30 : 50,
    spring: {
      damping: isVertical ? 15 : 12,
      stiffness: isVertical ? 200 : 100,
      mass: 1,
    },
    // 场景过渡
    sceneTransition: isVertical ? 8 : 15,
  },

  // ========== 布局偏好 ==========
  layout: {
    diagramRatio: isVertical ? 0.6 : 0.5,  // 图示占比
    textRatio: isVertical ? 0.4 : 0.5,     // 文字占比
    preferredSplit: isVertical ? 'SplitV' : 'SplitH',  // 首选分屏方式
    cardWidth: isVertical ? width * 0.85 : width * 0.45,
    iconSize: isVertical ? 48 : 40,
  },

  // ========== 安全区（避免被 UI 遮挡） ==========
  safeArea: {
    top: isVertical ? height * 0.1 : height * 0.05,
    bottom: isVertical ? height * 0.15 : height * 0.05,
    left: isVertical ? width * 0.05 : width * 0.08,
    right: isVertical ? width * 0.05 : width * 0.08,
  },

  // ========== 颜色系统 ==========
  colors: {
    // 背景
    bg1: '#0f0f23',
    bg2: '#1a1a3e',
    bg3: '#2d2d5a',
    
    // 强调色
    accent1: '#ff6b6b',  // 红
    accent2: '#4ecdc4',  // 青
    accent3: '#ffe66d',  // 黄
    accent4: '#95e1d3',  // 浅青
    accent5: '#a78bfa',  // 紫
    accent6: '#f97316',  // 橙
    
    // 文字
    white: '#ffffff',
    gray: '#94a3b8',
    dark: '#1e1e1e',
  },

  // ========== 便捷方法 ==========
  
  // 获取字幕样式字符串（用于 ffmpeg）
  getSubtitleStyle() {
    return `Fontname=${this.subtitle.fontName},FontSize=${this.subtitle.fontSize},MarginV=${this.subtitle.marginV},Alignment=${this.subtitle.alignment}`;
  },

  // 响应式字体计算
  getResponsiveFontSize(baseSize) {
    if (isVertical) {
      return Math.min(baseSize * 1.3, width * 0.06);
    }
    return baseSize;
  },

  // 检查是否在安全区内
  isInSafeArea(x, y, elementWidth, elementHeight) {
    return (
      x >= this.safeArea.left &&
      x + elementWidth <= width - this.safeArea.right &&
      y >= this.safeArea.top &&
      y + elementHeight <= height - this.safeArea.bottom
    );
  },
};

// 打印配置摘要
console.log('📐 视频配置:');
console.log(`   分辨率: ${width}×${height} (${isVertical ? '竖屏/移动端' : '宽屏/桌面端'})`);
console.log(`   标题字体: ${config.fonts.title}px`);
console.log(`   正文字体: ${config.fonts.body}px`);
console.log(`   字幕字体: ${config.subtitle.fontSize}px, 底部留白: ${config.subtitle.marginV}px`);
console.log(`   首选分屏: ${config.layout.preferredSplit}`);

module.exports = config;
