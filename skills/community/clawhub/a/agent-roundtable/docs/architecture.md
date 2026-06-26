# Roundtable 架构图

## 模块依赖关系

```
┌─────────────────────────────────────────────────────────────────────┐
│                        roundtable (Python Package)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                                   │
│  │ __init__.py  │  Public API exports                               │
│  └──────┬───────┘                                                   │
│         │                                                           │
│  ┌──────▼───────┐     ┌─────────────────┐     ┌──────────────────┐ │
│  │   models.py  │◄────│     core.py     │────►│   exceptions.py  │ │
│  │              │     │                 │     │                  │ │
│  │ Discussion   │     │ RoundtableCore  │     │ RoundtableError  │ │
│  │ Participant  │     │                 │     │ DiscussionNotFound│ │
│  │ Speech       │     │ create()        │     │ DiscussionNotActive│
│  │ Finding      │     │ speak()         │     │ InvalidParticipant│ │
│  │ Convergence  │     │ read()          │     │ InvalidSpeechOrder│ │
│  └──────────────┘     │ status()        │     │ InvalidFindingType│ │
│                       │ summarize()     │     │ InvalidReplyTo   │ │
│                       │ end_discussion()│     └──────────────────┘ │
│                       │ list()          │                           │
│  ┌──────────────┐     │ advance()       │     ┌──────────────────┐ │
│  │   db.py      │◄────│ notify()        │────►│   notify.py      │ │
│  │              │     │ run_demo()      │     │                  │ │
│  │ RoundtableDB │     └─────────────────┘     │ Notifier         │ │
│  │              │                              │ validate_config()│ │
│  │ SQLite store │                              │                  │ │
│  │ CRUD ops     │                              │ Event types:     │ │
│  │ Schema mgmt  │                              │  speech          │ │
│  └──────────────┘                              │  round_start     │ │
│                                               │  round_end       │ │
│  ┌──────────────────────────────────────┐     │  concluded       │ │
│  │         adapters/                    │     └──────────────────┘ │
│  │                                      │                          │
│  │  ┌──────────────┐  ┌──────────────┐  │                          │
│  │  │  generic.py  │  │  hermes.py   │  │                          │
│  │  │              │  │              │  │                          │
│  │  │ Roundtable   │  │ register_*() │  │                          │
│  │  │ (facade)     │  │ (Hermes MCP) │  │                          │
│  │  └──────────────┘  └──────────────┘  │                          │
│  └──────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

## 核心状态机

```
                    ┌──────────────┐
                    │   创建讨论    │
                    │ create_disc() │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
           ┌───────│    active     │◄──────────┐
           │       │ current_round │           │
           │       └──────┬───────┘           │
           │              │                    │
           │              ▼                    │
           │       ┌──────────────┐           │
           │       │  speak()     │           │
           │       │  add_speech  │           │
           │       └──────┬───────┘           │
           │              │                    │
           │      ┌───────┴────────┐          │
           │      │                │          │
           │      ▼                ▼          │
           │  round_complete   round_start    │
           │  (all spoke)     (1st speech)    │
           │      │                           │
           │      ▼                           │
           │  new_round > max?                │
           │   ├─ No  ───────────────────────┘
           │   │  (advance round)
           │   │
           │   ▼ Yes
           │  ┌──────────────┐
           │  │  auto_conclude│
           │  └──────┬───────┘
           │         │
           ▼         ▼
    ┌──────────┐  ┌──────────────┐
    │ cancelled│  │   concluded  │
    │ (force)  │  │  (normal)    │
    └──────────┘  └──────────────┘
```

## 数据流

```
  User/Agent                Core                  DB (SQLite)
     │                      │                       │
     │── create_disc() ────►│── INSERT disc ────────►│
     │◄── {disc_id} ────────│◄── {Discussion} ───────│
     │                      │                       │
     │── speak(id,who,txt)─►│── validate ───────────►│
     │                      │── INSERT speech ──────►│
     │                      │── check round_complete │
     │                      │── calc convergence ───►│
     │◄── {speech_id,round}─│                       │
     │                      │                       │
     │── read(id) ─────────►│── SELECT speeches ────►│
     │◄── {speeches,...} ───│◄── [Speech,...] ───────│
     │                      │                       │
     │── summarize(id) ────►│── SELECT all ─────────►│
     │                      │── build_structured ───►│
     │◄── {summary} ────────│                       │
     │                      │                       │
     │── end_disc(id) ─────►│── UPDATE status ──────►│
     │◄── {action} ─────────│                       │
     │                      │                       │
     │                      │── Notifier ──────────►│  send_fn(platform,chat,msg)
```

## 测试覆盖率 (v0.1.0a1)

| 模块                  | 语句数 | 未覆盖 | 覆盖率 |
|-----------------------|--------|--------|--------|
| core.py               | 386    | 1      | 99%    |
| db.py                 | 205    | 19     | 91%    |
| notify.py             | 113    | 9      | 92%    |
| models.py             | 53     | 0      | 100%   |
| exceptions.py         | 7      | 0      | 100%   |
| adapters/generic.py   | 60     | 42     | 30%    |
| adapters/hermes.py    | 100    | 60     | 40%    |
| **总计**              | **932**| **131**| **86%**|
