---
name: a2a-manager
description: Agent-to-Agent Manager dành cho Coordinator/Orchestrator. Sử dụng khi: (1) Tạo agent mới theo yêu cầu, (2) Quản lý Discord Category/Channel/Role, (3) Binding agent với channel, (4) Điều phối agent-to-agent, (5) Tạo/cập nhật A2A_MAP.md (từ template cứng trong script), (6) Spawn/dispose Specialists (sub-agents), (7) Quản lý task workflow với Notion.

Trigger phrases: "tạo agent", "tạo channel", "thêm nàng", "spawn specialist", "task board", "quản lý agent", "điều phối", "phân công", "A2A", "tìm agent", "cập nhật map"
---

# A2A Manager

## Trigger Phrases

| Trigger | Action |
|---------|--------|
| "tạo agent", "thêm nàng" | Tạo agent mới |
| "tạo channel" | Tạo Discord channel |
| "spawn specialist" | Tạo sub-agent tạm thời |
| "task board", "quản lý task" | Notion task management |
| "quản lý agent" | Agent registry management |
| "điều phối", "phân công" | Task orchestration |
| "A2A", "map" | A2A_MAP management |
| "tìm agent" | Lookup agent |

## Agent Types (Task-Steward Inspired)

### 1. Specialized Agents (Permanent)
> Core agents - Sống trong workspace, có identity riêng

- **Coordinator**: C.C. - Điều phối chính
- **Orchestrator**: Makima - Phối hợp nhiều agent
- **Worker**: Winry, Motoko - Thực thi task
- **QA**: Jalter, Violet - Verify chất lượng

### 2. Role-specific Agents
> Theo chức năng cụ thể

### 3. Specialists (Sub-agents)
> Tạm thời - Sinh ra để làm task cụ thể, xong.Dispose

| Type | Use Case | Model |
|------|----------|-------|
| temp_worker | Task đơn giản | flash |
| researcher | Nghiên cứu sâu | pro |
| coder | Code task | glm4 |
| qa_reviewer | Verify work | flash |
| runner | Chạy lệnh | flash |

## Workflow (Task-Steward với Notion)

### Task States
| State | Notion Status | Description |
|-------|---------------|-------------|
| NOW | Now/Today | Ưu tiên cao |
| WAITING | Waiting | Chờ input |
| IN_PROGRESS | In Progress | Đang làm |
| REVIEW | Ready for Review | Chờ QA |
| DONE | Done | Hoàn thành |

### Workflow
```
Master → Task Request
    ↓
C.C. (Coordinator) → Classify: Q&A or Task?
    ↓
Q&A → Answer immediately
Task → Notion Task Board → Execute (spawn Specialist) → QA → Deliver
```

## Scripts

### A2A Map
- `a2a_map.py` - Quản lý A2A_MAP.md
  - Template từ references/A2A_MAP.md
  - Validation: agent, model, status
  - Versioning + Rollback
  - Init tạo workspace/A2A_MAP.md từ template

### Task Board (Notion)
- `task_board.py` - Quản lý task trên Notion
  - Setup database
  - Create/Update/List tasks
  - Workflow: start, block, complete, approve, reject

### Discord
- `discord_manager.py` - Quản lý Category/Channel/Role

### Specialist Management
- `specialist_manager.py` - Spawn/dispose sub-agents

### Agent Creation
- `create_agent.py` - Tạo agent mới

## Quick Actions

### A2A Map
```bash
# Validate map
python a2a_map.py validate

# Versions
python a2a_map.py versions
```

### Task Board (Notion)
```bash
python task_board.py setup <database_id>
python task_board.py create "Fix bug" "Mô tả"
python task_board.py start <task_id>
python task_board.py complete <task_id>
python task_board.py approve <task_id>
```

### Specialists
```bash
python specialist_manager.py spawn coder "Fix bug" Winry
python specialist_manager.py list
python specialist_manager.py dispose <spec_id>
```

## Files

- [a2a_map.py](scripts/a2a_map.py) - Core map (template trong script)
- [task_board.py](scripts/task_board.py) - Notion task management
- [specialist_manager.py](scripts/specialist_manager.py) - Sub-agent management
- [create_agent.py](scripts/create_agent.py) - Agent creation
- [discord_manager.py](scripts/discord_manager.py) - Discord management
