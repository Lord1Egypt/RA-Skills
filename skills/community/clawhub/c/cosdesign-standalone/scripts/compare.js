#!/usr/bin/env node
/**
 * CosDesign — Multi-site Design Comparison
 * PROMPT GENERATOR ONLY — outputs a structured agent prompt.
 *
 * Usage:
 *   node scripts/compare.js <url1> <url2> [url3]
 */

const urls = process.argv.slice(2).filter(a => !a.startsWith('--'));

if (urls.length < 2) {
  console.error('Usage: node scripts/compare.js <url1> <url2> [url3]');
  console.error('  At least 2 URLs required for comparison.');
  process.exit(1);
}

const urlList = urls.map((u, i) => `  Site ${i + 1}: ${u}`).join('\n');
const siteLabels = urls.map((u, i) => {
  try { return new URL(u).hostname.replace('www.', ''); } catch { return `Site${i+1}`; }
});

console.log(`=== COSDESIGN — 多站设计风格对比 ===
对比站点：
${urlList}

你是一个专业的设计系统分析师。你的任务是对比 ${urls.length} 个网站的视觉设计风格。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一步 — 依次获取每个页面
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

对每个 URL，使用 WebFetch 获取页面内容，提取 CSS 样式信息：
${urls.map((u, i) => `
Site ${i+1}: ${u}
  WebFetch prompt: "Extract all visual design properties: colors, fonts, spacing, layout, border-radius, shadows from this page."`).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二步 — 逐维度对比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

对每个维度，列出各站点的值并标注差异：

1. 色彩对比
| 色彩角色 | ${siteLabels.join(' | ')} |
|----------|${siteLabels.map(() => '---').join('|')}|
| Primary | ... |
| Secondary | ... |
| Background | ... |
| Text | ... |
| Accent | ... |

2. 字体对比
| 项目 | ${siteLabels.join(' | ')} |
|------|${siteLabels.map(() => '---').join('|')}|
| Heading font | ... |
| Body font | ... |
| Base size | ... |
| Scale ratio | ... |

3. 间距对比
| Token | ${siteLabels.join(' | ')} |
|-------|${siteLabels.map(() => '---').join('|')}|
| Base unit | ... |
| Container width | ... |
| Section padding | ... |

4. 组件风格对比
| 组件 | ${siteLabels.join(' | ')} |
|------|${siteLabels.map(() => '---').join('|')}|
| Button border-radius | ... |
| Card shadow | ... |
| Input style | ... |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三步 — 风格总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

为每个站点写一段 2-3 句的风格定义，然后输出：

### 共同点
- 列出 2-3 个所有站点共享的设计特征

### 差异点
- 列出最显著的 3-5 个风格差异

### 推荐
如果要融合这些风格，建议采用哪些元素？给出具体参数。
`);
