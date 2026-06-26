# 文案生成流程

架构核心设计：
1. 文案生成时只加载轻量画像（~400 tokens），不全量读取profile.json
2. 知识库精准检索，只返回相关段落，不读整个文件
3. 系列文案连续性只读摘要，不读全文
4. 所有写入操作通过 `db_query.py` CLI 完成，智能体不可自行写文件或创建脚本

## 获取生成上下文

一条命令获取文案生成所需的全部数据：

```bash
python scripts/db_query.py --type context --lecturer 讲师A --query "养生保健" --data-dir <控制台目录>
```

返回：
- `profile`: 轻量画像（lecturer_name + qualitative + persona_mapping + style_dimensions）
- `reference_samples`: 参考示例
- `knowledge_context`: token预算内的精准知识段落
- `behavior_rules`: 行为规则（允许+禁止）

## 单篇文案生成

1. 获取生成上下文（上述命令）
2. 加载风格模板：见 [script-styles.md](script-styles.md)
3. 融合画像+参考示例+知识段落+风格 → 生成文案
4. 保存文案（单篇视为1集系列）：
   ```bash
   # 先创建系列计划（1集）
   python scripts/db_query.py --type series --action save_plan \
     --id "<文案主题>" --lecturer <讲师> \
     --query '{"title":"<主题>","episodes":[{"num":1,"title":"<标题>","topic":"<主题>"}]}' \
     --data-dir <控制台目录>
   # 再保存文案
   python scripts/db_query.py --type series --action save_episode \
     --id "<文案主题>" --id2 1 \
     --query '{"title":"<标题>","content":"<正文>","summary":"<100字摘要>","hook_next":""}' \
     --data-dir <控制台目录>
   ```

文案保存到 `控制台/讲师列表/{讲师}/系列文案/{主题}/E01_{标题}.txt`，路径由脚本强制控制。

## 系列文案

1. 获取生成上下文
2. 制定系列计划（智能体生成每集标题和主题）
3. 保存系列计划到数据库：
   ```bash
   python scripts/db_query.py --type series --action save_plan \
     --id <系列名> --lecturer <讲师> \
     --query '{"title":"<系列标题>","episodes":[{"num":1,"title":"第1集标题","topic":"主题"},{"num":2,"title":"第2集标题","topic":"主题"}]}' \
     --data-dir <控制台目录>
   ```
4. 查看系列计划：
   ```bash
   python scripts/db_query.py --type series --action get_plan --id <系列名> --data-dir <控制台目录>
   ```
5. 逐集生成，每集保存：
   ```bash
   python scripts/db_query.py --type series --action save_episode \
     --id <系列名> --id2 <集号> \
     --query '{"title":"<标题>","content":"<正文>","summary":"<100字摘要>","hook_next":"<下集衔接点>"}' \
     --data-dir <控制台目录>
   ```

**连续性优化**：生成第N集时只读前N-1集的摘要（每集~100字），不读全文。

```bash
# 查看系列摘要（连续性用）
python scripts/db_query.py --type series --action summaries --id <系列名> --data-dir <控制台目录>
```

## 修订流程（改集/删集）

当用户要求修改某集文案时，必须先删除旧数据再保存新数据。

### 修改第X集

1. 重新获取生成上下文（不要复用旧context）：
   ```bash
   python scripts/db_query.py --type context --lecturer <讲师> --query "<主题>" --data-dir <控制台目录>
   ```
2. 读取当前文案（了解原文内容）：
   ```bash
   python scripts/db_query.py --type series --action content --id <系列名> --id2 X --data-dir <控制台目录>
   ```
3. 删除旧集数据（必须！否则DB出现重复记录）：
   ```bash
   python scripts/db_query.py --type series --action delete_episode --id <系列名> --id2 X --data-dir <控制台目录>
   ```
4. 根据用户要求修改文案
5. 保存修改后的文案：
   ```bash
   python scripts/db_query.py --type series --action save_episode \
     --id <系列名> --id2 X \
     --query '{"title":"<标题>","content":"<正文>","summary":"<100字摘要>","hook_next":"<下集衔接>"}' \
     --data-dir <控制台目录>
   ```

**关键**：`delete_episode` 必须在 `save_episode` 之前执行。跳过 `delete_episode` 会导致DB重复记录和旧的.txt文件残留。

进度计数器自动处理：修订中间集（如第2集）不会导致进度倒退，因为进度取的是 MAX(episode_num)。

### 删除某集

```bash
python scripts/db_query.py --type series --action delete_episode --id <系列名> --id2 X --data-dir <控制台目录>
```

删除操作会：移除DB元数据 + 删除.txt文件 + 自动更新进度计数器。

## 系列进度

```bash
python scripts/db_query.py --type series --action progress --id <系列名> --data-dir <控制台目录>
python scripts/db_query.py --type series --action list --data-dir <控制台目录>
```
