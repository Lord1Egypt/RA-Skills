# Install examples

## Example A: management-only deployment

```bash
clawhub install ceo-xiaomao-agent
mkdir -p ~/workspace/ceo-xiaomao
cd ~/workspace/ceo-xiaomao
python3 ~/.openclaw/skills/ceo-xiaomao-agent/scripts/init_agent_workspace.py
```

## Example B: management + execution bundle

```bash
clawhub install ceo-xiaomao-agent
clawhub install ceo-xiaomao
mkdir -p ~/workspace/ceo-team
cd ~/workspace/ceo-team
python3 ~/.openclaw/skills/ceo-xiaomao-agent/scripts/init_agent_workspace.py
```

## Example C: first prompt

```text
请以CEO小茂身份启动，读取工作区后，用“结论 / 当前进展 / 下一步 / 风险点”格式向我汇报。
```
