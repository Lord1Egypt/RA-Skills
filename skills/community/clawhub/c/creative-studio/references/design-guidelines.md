# 萤火虫空压机 - 品牌设计规范

## 品牌信息

- 公司全称：广州市萤火虫智能装备技术有限公司
- 简称：萤火虫空压机
- 英文：Firefly Air Compressor (Guangzhou Firefly Intelligent Equipment Technology Co., Ltd.)
- 网址：http://www.fireflies.net.cn
- 服务热线：13825202084（邹先生）
- 邮箱：aifirefly@163.com
- 地址：广州市
- 品牌理念："节能自然萤火虫" — 为客户节资、为环境减排

## 色彩系统

### 主色调
| 名称 | HEX | RGB | CSS变量 | 用途 |
|------|-----|-----|---------|------|
| 品牌绿 Primary | #1B8C3A | 27,140,58 | `--color-primary` | 主按钮、标题强调、图表主色 |
| 深绿 Primary Dark | #0E5C25 | 14,92,37 | `--color-primary-dark` | 页脚背景、深色强调 |
| 浅绿 Primary Light | #4CAF50 | 76,175,80 | `--color-primary-light` | 图标、标签、装饰 |
| 绿背景 Primary BG | #E8F5E9 | 232,245,233 | `--color-primary-bg` | 卡片背景、信息条 |

### 辅色调
| 名称 | HEX | RGB | CSS变量 | 用途 |
|------|-----|-----|---------|------|
| 科技蓝 Secondary | #1565C0 | 21,101,192 | `--color-secondary` | 链接、数据可视化 |
| 深蓝 Secondary Dark | #0D47A1 | 13,71,161 | `--color-secondary-dark` | 深色面板 |
| 浅蓝 Secondary Light | #42A5F5 | 66,165,245 | `--color-secondary-light` | 信息提示 |

### 强调色
| 名称 | HEX | RGB | CSS变量 | 用途 |
|------|-----|-----|---------|------|
| 活力橙 Accent | #F57C00 | 245,124,0 | `--color-accent` | CTA按钮、价格、限时标签 |
| 深橙 Accent Hover | #E65100 | 230,81,0 | `--color-accent-hover` | 悬停状态 |

### 中性色
| 名称 | HEX | 用途 |
|------|-----|------|
| #1A1A1A | 主文字 | 标题、正文 |
| #555555 | 次要文字 | 描述、标签 |
| #888888 | 辅助文字 | 脚注、时间戳 |
| #FAFAFA | 浅灰背景 | 页面底色 |
| #F0F2F5 | 灰色背景 | 区块分隔 |
| #E0E0E0 | 边框 | 卡片边框、分割线 |
| #FFFFFF | 白色 | 卡片、弹窗背景 |

## 字体层级

### 中文字体栈
```
"PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", "Helvetica Neue", Arial, sans-serif
```

### 字号规范
| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 2.5rem (40px) | 1.25 | Bold 700 | 页面主标题 |
| H2 | 2rem (32px) | 1.25 | Bold 700 | 区块标题 |
| H3 | 1.5rem (24px) | 1.25 | SemiBold 600 | 卡片标题 |
| H4 | 1.25rem (20px) | 1.25 | Medium 500 | 组件标题 |
| Body | 1rem (16px) | 1.6 | Regular 400 | 正文 |
| Small | 0.875rem (14px) | 1.6 | Regular 400 | 辅助文字 |
| XS | 0.75rem (12px) | 1.6 | Regular 400 | 脚注、标签 |

## 间距系统

| Token | 值 | 用途 |
|-------|-----|------|
| xs | 4px | 图标与文字间距 |
| sm | 8px | 紧凑间距 |
| md | 16px | 默认内边距 |
| lg | 24px | 卡片间距 |
| xl | 32px | 大区块间距 |
| 2xl | 48px | 内容区间距 |
| 3xl | 64px | 章节间距 |
| 4xl | 96px | 页面级间距 |

## 圆角

| Token | 值 | 用途 |
|-------|-----|------|
| sm | 4px | 小标签、徽章 |
| md | 8px | 按钮、输入框 |
| lg | 12px | 卡片、面板 |
| xl | 20px | 大容器、弹窗 |
| full | 50% | 头像、圆形图标 |

## 阴影

| Token | 值 | 用途 |
|-------|-----|------|
| xs | 0 1px 2px rgba(0,0,0,0.05) | 微妙层次 |
| sm | 0 1px 3px rgba(0,0,0,0.10) | 卡片默认 |
| md | 0 4px 6px rgba(0,0,0,0.07) | 浮层 |
| lg | 0 10px 15px rgba(0,0,0,0.10) | 弹窗 |
| xl | 0 20px 40px rgba(0,0,0,0.12) | 模态框 |
| card-hover | 0 8px 30px rgba(0,0,0,0.12) | 卡片悬停 |

## 通用组件模式

### 主按钮
```css
.btn-primary {
  background: #1B8C3A;
  color: #FFFFFF;
  padding: 12px 28px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}
.btn-primary:hover { background: #0E5C25; }
```

### 卡片
```css
.card {
  background: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.10);
  transition: box-shadow 0.3s ease;
}
.card:hover {
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}
```

### 数据指标卡
```css
.metric-card {
  text-align: center;
  padding: 20px;
}
.metric-card__value { font-size: 2rem; font-weight: 700; color: #1B8C3A; }
.metric-card__label { font-size: 0.875rem; color: #888888; }
```

### 特性网格
- 2列：移动端
- 3列：平板（≥768px）
- 4列：桌面（≥1024px）

## 详情页布局

推荐的详情页从上到下布局：
1. **Hero** — 产品主图 + 名称 + 一句话卖点
2. **规格表** — 技术参数表格，绿色表头
3. **特性卡片** — 3-4个卖点卡片（图标+标题+描述）
4. **3D展示** — 可选 Three.js 交互区
5. **CTA** — 咨询热线 + 按钮
6. **页脚** — 公司信息 + 版权

## 输出规范

- 所有金额以"万元"为单位，保留1位小数
- 所有百分比保留整数
- HTML 文件自包含（所有 CSS/JS 内联）
- 图片使用相对路径或 base64
- 打印友好的 @media print 样式
- 响应式断点：768px、1024px
