# Localization Rules

Cognitive function codes (Ti, Te, Fi, Fe, Ni, Ne, Si, Se) always keep their English
abbreviations in all languages. ALL structural/positional terms MUST be translated.

## Chinese Translation Table

| English term       | 中文翻译（必须使用） |
|--------------------|---------------------|
| dom / dominant     | 主导                |
| aux / auxiliary    | 辅助                |
| tert / tertiary    | 第三功能             |
| inf / inferior     | 劣势功能             |
| function stack     | 功能栈              |
| observer lens      | 观察者视角           |
| grip / in the grip | 劣势功能掌控状态      |
| shadow function    | 影子功能             |

## Format Rules

**Chinese**: `<Function代码> + 空格 + <中文位置词>`。多个功能之间用`、`（顿号）分隔。

✅ `Te 主导、Se 辅助` · `Ti 主导、Ne 辅助、Si 第三功能、Fe 劣势功能`
❌ `Te-dom，Se-aux` · `Te dom aux` · `Te主导-Se辅助`

**English (unchanged)**: `Te-dom, Se-aux` / `Ti-Ne` / `Fe inferior`

**Other languages**: Same principle — translate positional labels, keep function codes.

## Mandatory Self-Check Before Sending Non-English Output

1. Search draft for: `dom`, `aux`, `tert`, `inf`, `grip`, `stack`, `dominant`,
   `auxiliary`, `tertiary`, `inferior`
2. If any appear next to a function code or in descriptive prose about cognitive
   functions → replace with target-language equivalent
3. Verify multiple functions use appropriate list separator (Chinese: `、`)
4. Only send after this scan passes
