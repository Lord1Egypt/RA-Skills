# Fund Keeper v2.3 更新说明

## 🎉 新增功能 (v2.3)

### 1. 收益统计 📊

**命令**: `py fund_keeper.py stats`

**功能**:
- 总投入/当前值/累计收益
- 收益率计算
- 收益贡献排名
- 定投基金统计

**输出示例**:
```
============================================================
【收益统计】2026-03-07 20:24
============================================================

总投入：  9,066.21 元
当前值：  9,287.23 元
累计收益：+221.02 元 (+2.44%)
持有基金：4 支 (2 支定投)
收益贡献王：017470 嘉实科创板芯片 ETF 联接 C (+188.40 元)

【收益贡献排名】
------------------------------------------------------------
1. 017470 嘉实科创板芯片 ETF 联接 C  +188.40 [+]x42 +85.2%
2. 000218 国泰黄金 ETF 联接 A     +49.01 [+]x11 +22.2%
3. 270042 广发纳斯达克 100ETF    -5.28 [-]x1 -2.4%
4. 011608 易方达科创 50 联接 A     -11.11 [-]x2 -5.0%

============================================================
```

---

### 2. 定投计划管理 📅

**命令**: `py fund_keeper.py sip [操作]`

#### 列出定投计划
```bash
py fund_keeper.py sip --list
```

#### 添加定投计划
```bash
py fund_keeper.py sip --add --fund 011608 --name "科创 50" --amount 500 --day 15
```

**参数**:
- `--fund`: 基金代码（必填）
- `--name`: 基金名称（可选）
- `--amount`: 定投金额（必填）
- `--day`: 每月定投日 1-28（必填）

#### 暂停定投计划
```bash
py fund_keeper.py sip --pause 011608
```

#### 恢复定投计划
```bash
py fund_keeper.py sip --resume 011608
```

#### 删除定投计划
```bash
py fund_keeper.py sip --delete 011608
```

**输出示例**:
```
============================================================
【定投计划】
============================================================

【进行中】
  011608 科创 50             500 元/月  每月 15 日

============================================================
月度定投总额：500 元
============================================================
```

---

## 📁 新增文件

| 文件 | 说明 |
|------|------|
| `fund_stats.py` | 收益统计与定投管理核心 |
| `funds/stats.json` | 收益统计缓存 |
| `funds/sip-plan.json` | 定投计划配置 |
| `funds/sip-record.md` | 定投操作记录 |

---

## 🔄 完整命令列表

```bash
# 持仓查询
py fund_keeper.py portfolio              # 查看持仓
py fund_keeper.py portfolio --cross-validate  # 交叉验证模式

# 投资建议
py fund_keeper.py advice                 # 全部建议
py fund_keeper.py advice --fund 000218   # 单基金建议

# 收益统计 (NEW!)
py fund_keeper.py stats                  # 收益统计

# 定投管理 (NEW!)
py fund_keeper.py sip --list             # 列出定投计划
py fund_keeper.py sip --add --fund XXX --amount 500 --day 15  # 添加
py fund_keeper.py sip --pause XXX        # 暂停
py fund_keeper.py sip --resume XXX       # 恢复
py fund_keeper.py sip --delete XXX       # 删除

# 其他
py fund_keeper.py ocr --image xxx.png    # OCR 识图
py fund_keeper.py add --image xxx.png    # 识图添加
```

---

## 📊 使用场景

### 场景 1: 查看今日收益
```bash
py fund_keeper.py stats
```

### 场景 2: 设置定投计划
```bash
# 每月 15 日定投科创 50 基金 500 元
py fund_keeper.py sip --add --fund 011608 --name "科创 50" --amount 500 --day 15

# 每月 10 日定投黄金基金 1000 元
py fund_keeper.py sip --add --fund 000218 --name "黄金" --amount 1000 --day 10
```

### 场景 3: 暂停定投
```bash
# 市场高位，暂停定投
py fund_keeper.py sip --pause 011608

# 市场回调，恢复定投
py fund_keeper.py sip --resume 011608
```

### 场景 4: 查看定投记录
```bash
# 查看定投操作历史
cat funds/sip-record.md
```

---

## 🎯 下一步优化

### P1 - 已完成 ✅
- [x] 收益统计
- [x] 定投计划管理

### P2 - 待实现
- [ ] 收益趋势图（matplotlib）
- [ ] 自动定投执行
- [ ] 飞书消息推送
- [ ] 风险评估

---

## ⚠️ 注意事项

1. **编码问题**: Windows 控制台使用 GBK 编码，中文可能显示为乱码
   - 不影响功能，数据正常保存
   - 建议：PowerShell 中使用 `chcp 65001` 切换 UTF-8

2. **定投执行**: 当前仅记录计划，不自动执行
   - 需要手动买入
   - 未来版本将支持自动定投

3. **数据更新**: 收益统计基于 `my-funds.md` 中的数据
   - 定期更新持仓数据
   - 或使用 OCR 自动识别

---

*版本：v2.3 | 更新日期：2026-03-07*
