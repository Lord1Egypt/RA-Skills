# ================================
# fanzhi-provenance: fz:skill:e6f788c2:wsl_lobster:mpc2j3a6
# project: html-to-pdf v1.0.4
# content-hash: e6f788c2
# license: MIT-0 (ClawHub)
# copyright: 泛智生态 / Ronie & 泛智小龙虾
# fanzhi-signature: (Phase 3)
# ================================

# 来源与参考 - 许可声明

## 直接依赖（代码引用）

| 项目 | 协议 | 链接 |
|------|------|------|
| puppeteer-core | Apache-2.0 | https://github.com/puppeteer/puppeteer |
| pdf-lib | MIT | https://github.com/Hopding/pdf-lib |

### 遵守条款

- **puppeteer-core（Apache-2.0）**：import 调用 API，不修改库本身，不二次分发。保留上游 NOTICE 义务。
- **pdf-lib（MIT）**：import `PDFDocument` 读取验证 PDF。按 MIT 条款保留版权声明。

## 二进制依赖

| 项目 | 协议 | 说明 |
|------|------|------|
| Chromium | BSD-3-Clause | `puppeteer.launch()` 启动为 headless 渲染引擎 |

## 方案调研参考（未引用代码）

| 项目 | 协议 | 链接 | 评估结论 |
|------|------|------|---------|
| jsPDF | MIT | parallax/jsPDF | 中文需字体子集化，未采纳 |
| pdfmake | MIT | bpampuch/pdfmake | 同上，未采纳 |
| HTMX | BSD-2-Clause | bigskysoftware/htmx | UI 框架参考，未用于 PDF |
| Pico.css | MIT | picocss/pico | CSS 框架参考，未使用 |
| mini.css | MIT | mini-css/mini.css | CSS 框架参考，未使用 |

## 本技能协议

MIT-0（ClawHub 默认），与上游库无协议冲突。
