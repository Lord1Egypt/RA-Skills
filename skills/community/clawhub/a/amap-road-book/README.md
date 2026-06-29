<p align="center">
  <img src="assets/logo.png" alt="Amap Roadbook Skill Logo" width="128" />
</p>

<h1 align="center">Amap Roadbook Skill</h1>

<p align="center">
  用自然语言生成高德地图路书：在线预览、实时编辑、真实路线、天气提醒和 Excel 计划表一次完成。
</p>

<p align="center">
  <a href="https://docs.openclaw.ai/clawhub/skill-format"><img alt="OpenClaw Skill" src="https://img.shields.io/badge/OpenClaw-Skill-111827?style=flat-square"></a>
  <img alt="Amap" src="https://img.shields.io/badge/Amap-Web%20Service%20%2B%20JS%20API-1677ff?style=flat-square">
  <img alt="Node" src="https://img.shields.io/badge/Node.js-18%2B-339933?style=flat-square">
  <img alt="License" src="https://img.shields.io/badge/License-ISC-f59e0b?style=flat-square">
</p>

<p align="center">
  <img src="https://sop26.oss-cn-hangzhou.aliyuncs.com/oss/image/open-close-store/896499fefaf24a52959e5d62c21ecee4.png" alt="Amap Roadbook Skill Preview" width="860" />
</p>

---

## ClawHub 安装

在 ClawHub 中启用 `amap-roadbook` 后，建议在 `~/.openclaw/openclaw.json` 里写入下面的推荐配置：

```json5
{
  skills: {
    entries: {
      "amap-roadbook": {
        enabled: true,
        env: {
          AMAP_WEB_SERVICE_KEY: "YOU_AMAP_WEB_SERVICE_KEY",
          AMAP_JS_API_KEY: "YOUR_AMAP_JS_API_KEY",
          AMAP_JS_SECURITY_CODE: "YOUR_AMAP_JS_SECURITY_CODE"
        }
      }
    }
  }
}
```

## 它能做什么

`amap-roadbook` 是一个面向 OpenClaw / ClawHub 的旅行路书 Skill。你可以直接用一句旅行想法，让它帮你生成一份可执行的高德地图路书。

它会在信息不足时先反问关键问题；信息足够后，会结合高德 API 做地点解析、POI 查询、路线规划、天气提醒、每日时间线，并输出可分享的 HTML 地图页面、结构化 JSON 和 Excel 表格。

适合这些场景：

- 把“我想去某地玩几天”变成按天执行的行程。
- 为景点、酒店、车站、机场之间规划交通衔接。
- 生成带地图线路的可分享路书页面。
- 在线预览和实时编辑路书，边看地图边调整每日安排。
- 导出 Excel 计划表，方便同行人查看、打印或二次编辑。
- 在路线接口查不到完整路径时，自动使用直线兜底，保证地图仍然可读。

## 功能亮点

- **自然语言转路书**：从旅行想法生成结构化行程。
- **高德真实数据**：使用地理编码、POI、路径规划、天气等高德 Web Service API。
- **交互地图页面**：基于高德 JS API 渲染停靠点、路线和每日行程。
- **在线预览**：生成可分享的网站页面，打开链接即可查看完整地图路书。
- **实时编辑**：修改行程后可复用同一个发布地址覆盖更新，适合反复打磨路线。
- **路线容错**：优先使用真实线路，查不到时自动兜底，不让地图断线。
- **Excel 计划表**：生成总览、每日行程、路线段、预算、景点信息等 Sheet。
- **公网发布**：可生成可访问的 HTML/JSON/XLSX 链接。
- **隐私友好**：不内置任何作者 Key，所有高德 Key 由用户在本地配置。

## 目录结构

```text
amap-roadbook/
  SKILL.md                    # OpenClaw Skill 定义与执行说明
  assets/
    roadbook.html             # 交互式地图路书模板
  scripts/
    plan-roadbook.mjs         # 路书生成、路线增强、发布入口
    export-excel.mjs          # Excel 导出脚本
    publish-server.mjs        # 可选的发布服务端
  references/
    amap-api-map.md           # 高德 API 使用映射
    clarification-policy.md   # 反问策略
    roadbook-schema.md        # 路书 JSON Schema 说明
    demo-scenarios.md         # 示例场景
  agents/
    openai.yaml               # Agent 配置
```

## 安装

本地开发时可以直接克隆仓库：

```bash
git clone https://github.com/zuo-wentao/Amap-Roadbook-Skill.git
cd Amap-Roadbook-Skill
npm install
```

如果你要在本地让 OpenClaw 扫描这个目录，再额外加 `extraDirs`：

```json5
{
  skills: {
    load: {
      extraDirs: [
        "/path/to/skill-parent-dir"
      ]
    }
  }
}
```

## 高德 Key 配置

这个 Skill 需要三个高德配置项，全部为必填：

| 环境变量 | 用途 |
|---|---|
| `AMAP_WEB_SERVICE_KEY` | 地理编码、POI、路线规划、天气等 Web Service API |
| `AMAP_JS_API_KEY` | 前端交互地图渲染 |
| `AMAP_JS_SECURITY_CODE` | 高德 JS API 安全密钥 |

推荐写到 `~/.openclaw/openclaw.json`：

```json5
{
  skills: {
    entries: {
      "amap-roadbook": {
        enabled: true,
        env: {
          AMAP_WEB_SERVICE_KEY: "YOU_AMAP_WEB_SERVICE_KEY",
          AMAP_JS_API_KEY: "YOUR_AMAP_JS_API_KEY",
          AMAP_JS_SECURITY_CODE: "YOUR_AMAP_JS_SECURITY_CODE"
        }
      }
    }
  }
}
```

也可以在 Shell 里临时配置：

```bash
export AMAP_WEB_SERVICE_KEY="你的高德 Web Service Key"
export AMAP_JS_API_KEY="你的高德 JS API Key"
export AMAP_JS_SECURITY_CODE="你的高德 JS 安全密钥"
```

高德 Key 可在 [高德开放平台](https://lbs.amap.com/) 申请：

- Web Service Key：平台选择「Web 服务」。
- JS API Key：平台选择「Web 端(JSAPI)」，并启用安全密钥。

## 使用方式

在 OpenClaw 中可以这样描述需求：

```text
使用 amap-roadbook。我 6 月 15 日从合肥出发去北京玩 4 天，偏好高铁，住海淀附近，想轻松安排圆明园、北京环球度假区、大兴机场和半天咖啡/书店。
```

如果信息不足，Skill 会先确认出发地、目的地、日期、必去地点、住宿区域、交通偏好等关键条件。

## 本地生成

准备输入 JSON 后，可以直接运行：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --output-dir output --excel
```

本地模式会生成：

```text
output/
  roadbook.html
  roadbook.json
  roadbook.xlsx
```

## 公网发布

发布模式会生成可访问的 HTML 页面和 Excel 下载链接：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --publish --excel
```

如需覆盖同一个发布目录，传入已有 `publishId`：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --publish --publish-id <previousPublishId> --excel
```

发布客户端可配置：

| 环境变量 | 说明 |
|---|---|
| `ROADBOOK_PUBLISH_TOKEN` | 上传服务鉴权 token |
| `ROADBOOK_PUBLISH_ENDPOINT` | 上传接口，默认使用 Skill 内置配置 |

公网链接可能包含出行日期、住宿区域、同行人、预算等敏感信息。只把发布链接分享给可信对象。

## Excel 内容

生成的 `roadbook.xlsx` 包含：

| Sheet | 内容 |
|---|---|
| 总览 | 目的地、日期、天气、预算、假设、提醒 |
| 每日行程 | 每日时间线，停靠点和交通衔接 |
| 路线段 | 起点、终点、交通方式、耗时、距离 |
| 预算 | 分项估算与合计 |
| 景点信息 | 电话、评分、营业时间等 POI 信息 |

也可以单独导出 Excel：

```bash
node scripts/export-excel.mjs --input output/roadbook.json --output output/roadbook.xlsx
```

## 发布到 ClawHub

仓库里已经提供 `.clawhubignore`，用于排除本地依赖、输入、输出和临时文件。

发布时应该包含：

- `SKILL.md`
- `assets/`
- `scripts/`
- `references/`
- `agents/openai.yaml`
- `package.json`
- `package-lock.json`

不应该包含：

- `node_modules/`
- `input/`
- `output/`
- `.agents/`
- `.git/`
- 日志、临时文件和任何真实 API Key

## 安全说明

请不要把真实的高德 Key、发布 token、个人行程数据提交到仓库。示例配置里只保留占位符，真实配置应写在本机环境变量或 `~/.openclaw/openclaw.json` 中。

## License

ISC
