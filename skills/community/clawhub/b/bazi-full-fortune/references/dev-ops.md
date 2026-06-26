# 开发运维

排盘脚本开发、ClawHub 发布、本地同步等运维事项。

---

# 一、cantian-tymext API

## 字段名为中文

`buildBaziFromSolar()` 返回对象使用中文字段名：

```typescript
// ❌ 错误 — 这些字段不存在
bazi.yearPillar
bazi.dayPillar

// ✅ 正确 — 中文字段名
bazi.年柱.天干.天干  // → "庚"
bazi.年柱.地支.地支  // → "辰"
bazi.月柱.天干.天干  // → "戊"
```

## 完整字段结构示例

```json
{
  "性别": 1, "阳历": "...", "农历": "...", "八字": "...", "生肖": "猴", "日主": "甲",
  "年柱": { "天干": { "天干": "甲", "五行": "木", "阴阳": "阳", "十神": "比肩" }, "地支": { "地支": "申", ... } },
  "月柱": { ... }, "日柱": { ... }, "时柱": { ... },
  "胎元": ..., "胎息": ..., "命宫": ..., "身宫": ..., "神煞": [...], "大运": [...], "刑冲合会": {...}
}
```

## try/catch 静默吞错

`try/catch` 可能将 `TypeError: Cannot read properties of undefined` 静默吞掉，导致表面看到 0 matches 而不报错。编写 scan_year 类脚本时，至少 log 非日期相关的错误。

> 经验教训：scan_year.ts 曾用 `bazi.yearPillar.toString()` 导致所有反推扫描永远返回 0 matches。

---

# 二、本地 skill 与 GitHub 仓库同步

PR 合并只更新 GitHub 仓库，不会自动更新本地 skill。每次合并后手动同步：

```bash
# 同步脚本
cp ~/Documents/bazi-full-fortune/scripts/*.ts ~/.hermes/skills/divination/bazi-full-fortune/scripts/

# 同步参考文档
cp ~/Documents/bazi-full-fortune/references/*.md ~/.hermes/skills/divination/bazi-full-fortune/references/
```

ClawHub 发布也需要手动同步后重新 publish。

---

# 三、ClawHub 发布

## Frontmatter 必须纯 ASCII

ClawHub 后端（Convex DB）不接受非 ASCII 字符作为字段名。

```bash
# ❌ 会失败
clawhub publish . --name "八字全方位算命" --tags "bazi,八字,命理"

# ✅ 正确
clawhub publish . --name "Bazi Full Fortune Telling" --tags "bazi,fortune-telling,chinese-astrology"
```

规则：
- `tags` 只用英文
- `name` 用英文
- 中文放在 `description` 里（description 支持 Unicode）

---

# 四、前置依赖

- 推荐运行环境：Node 24（可直接运行 TypeScript 源码）
- 兼容方案：若 Node 版本较低，使用 `tsx` 执行

```bash
npm install

# 仅在需要兼容运行时安装
# npm install -D tsx
```

---

# 五、脚本清单

| 脚本 | 功能 |
|------|------|
| `scripts/buildBaziFromSolar.ts` | 阳历排盘 |
| `scripts/buildBaziFromLunar.ts` | 农历排盘（不支持闰月） |
| `scripts/getChineseCalendar.ts` | 黄历查询 |
| `scripts/scan_year.ts` | 反推阳历日期 |
| `scripts/util.ts` | 公共参数解析 |

---

# 六、npm scripts 快捷方式

```bash
npm run bazi:solar -- "2000-12-22T03:30:00" 0 2
npm run bazi:lunar -- "2000-11-27T03:30:00" 0 2
npm run calendar
npm run calendar -- 2024-02-10
npm run scan -- 2000 0 --day-pillar 甲寅 --hour 03:30:00
```

---

# 七、注意事项

1. 所有命令均在项目根目录执行
2. 时间字符串不要携带时区后缀（如 `Z`、`+08:00`），以免产生与预期不一致的换日结果
3. 涉及 23:00-23:59 出生时，建议显式传 `sect`，避免晚子时归属歧义
4. 农历闰月必须先转阳历再用 `buildBaziFromSolar.ts`
5. 反推扫描请用 `scan_year.ts`（纯 TypeScript，无需 Python）
