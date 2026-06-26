# 常见问题 (FAQ)

## 一般问题

### Q1: 这个技能是做什么的？
**A:** 这个技能帮助您记录、管理和提醒食品过期情况。您可以：
- 记录购买的食品信息（名称、生产日期、保质期、存放位置等）
- 检查食品是否已过期或即将过期
- 获取一周内将过期的食品提醒
- 查看所有食品的详细清单和状态

### Q2: 数据存储在哪里？
**A:** 所有食品数据存储在 `技能目录/data/food_data.json` 文件中。这是一个JSON格式的文件，易于阅读和备份。

### Q3: 需要安装额外的依赖吗？
**A:** 不需要。这个技能使用Python标准库，不需要安装额外的包。

## 安装和设置

### Q4: 如何开始使用？
**A:** 按照以下步骤：
1. 确保技能目录存在：`~/.openclaw/workspace/skills/food-expiry-reminder`
2. 运行初始化脚本：`python scripts/init_data.py`
3. 开始添加食品：`python scripts/add_food.py ...`

### Q5: 如何验证安装是否成功？
**A:** 运行以下命令检查：
```bash
cd ~/.openclaw/workspace/skills/food-expiry-reminder
python scripts/init_data.py
python scripts/list_foods.py
```
如果看到"还没有添加任何食品"的提示，说明安装成功。

## 使用问题

### Q6: 添加食品时出现"日期格式错误"怎么办？
**A:** 确保生产日期使用正确的格式：`YYYY-MM-DD`
- ✅ 正确：`2024-03-04`
- ❌ 错误：`2024/03/04`、`04-03-2024`、`March 4, 2024`

### Q7: 如何批量添加食品？
**A:** 有几种方法：
1. 多次运行 `add_food.py` 脚本
2. 直接编辑 `data/food_data.json` 文件
3. 创建批处理脚本

### Q8: 如何更新食品信息？
**A:** 目前需要直接编辑 `data/food_data.json` 文件。未来版本可能会添加编辑功能。

### Q9: 如何删除食品？
**A:** 直接编辑 `data/food_data.json` 文件，从 `foods` 数组中删除对应的食品对象。

### Q10: 数据会丢失吗？
**A:** 数据存储在本地文件中，不会自动删除。但建议定期备份 `food_data.json` 文件。

## 功能问题

### Q11: 如何设置每天自动提醒？
**A:** 可以使用cron任务：
```bash
# 编辑crontab
crontab -e

# 添加以下行（每天上午9点检查）
0 9 * * * cd /path/to/skills/food-expiry-reminder && python scripts/get_reminders.py
```

### Q12: 可以设置不同的提醒时间吗？
**A:** 是的，可以修改 `check_expiry.py` 脚本中的时间阈值：
- 默认：一周内过期会提醒
- 可以修改为3天、10天等

### Q13: 如何查看特定位置的食品？
**A:** 目前需要查看完整列表然后筛选。未来版本可能会添加按位置筛选的功能。

### Q14: 可以导出数据吗？
**A:** 可以，`food_data.json` 本身就是标准JSON格式，可以直接复制或导入到其他系统。

### Q15: 支持多个用户吗？
**A:** 目前是单用户系统。如果需要多用户，可以为每个用户创建单独的数据文件。

## 故障排除

### Q16: 运行脚本时出现"没有那个文件或目录"错误
**A:** 确保在正确的目录中运行：
```bash
cd ~/.openclaw/workspace/skills/food-expiry-reminder
python scripts/脚本名称.py
```

### Q17: 出现"数据文件不存在"错误
**A:** 运行初始化脚本：
```bash
python scripts/init_data.py
```

### Q18: Python版本有问题
**A:** 这个技能需要Python 3.6或更高版本。检查Python版本：
```bash
python3 --version
```

### Q19: JSON文件格式错误
**A:** 如果手动编辑JSON文件导致格式错误，可以：
1. 使用JSON验证工具检查
2. 从备份恢复
3. 重新初始化并重新添加数据

### Q20: 脚本没有执行权限
**A:** 添加执行权限：
```bash
chmod +x scripts/*.py
```

## 高级用法

### Q21: 如何集成到OpenClaw的日常检查中？
**A:** 可以修改 `HEARTBEAT.md` 文件，添加食品检查：
```markdown
# 每天检查食品过期情况
运行食品过期检查脚本
```

### Q22: 可以添加自定义字段吗？
**A:** 可以，直接修改 `food_data.json` 文件的数据结构，但需要相应更新脚本。

### Q23: 如何备份数据？
**A:** 建议定期备份：
```bash
# 备份到其他位置
cp data/food_data.json ~/backups/food_data_backup.json

# 或使用版本控制
cd ~/.openclaw/workspace/skills/food-expiry-reminder
git add data/food_data.json
git commit -m "备份食品数据"
```

### Q24: 数据文件太大怎么办？
**A:** 定期清理已处理（已食用或丢弃）的食品记录。

### Q25: 可以添加图片或条形码吗？
**A:** 当前版本不支持，但可以在 `notes` 字段中添加相关信息的文字描述。

## 功能建议

### Q26: 未来可能添加的功能
**A:** 计划中的功能包括：
1. 图形用户界面 (GUI)
2. 移动端应用
3. 条形码扫描
4. 食谱建议（基于现有食材）
5. 购物清单生成
6. 营养信息跟踪

### Q27: 如何贡献代码？
**A:** 欢迎提交改进建议和代码贡献。可以：
1. Fork项目
2. 实现新功能
3. 提交Pull Request

### Q28: 在哪里报告问题？
**A:** 可以通过OpenClaw的反馈渠道报告问题。

### Q29: 有使用教程视频吗？
**A:** 目前只有文字文档。未来可能会制作视频教程。

### Q30: 这个技能是免费的吗？
**A:** 是的，完全免费和开源。