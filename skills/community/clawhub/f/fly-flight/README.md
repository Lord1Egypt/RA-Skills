# Fly Flight

An OpenClaw skill for querying China domestic transport in one place.  
一个用于查询中国境内出行信息的 OpenClaw skill。

This version supports both flights and high-speed rail in one unified transport skill.  
这个版本已经把航班和高铁统一进同一个 transport skill 里。

## Requirements | 依赖环境

This skill requires the following runtime dependencies:

- `python3`
- `node`
- Network access to public flight pages and official 12306 endpoints

这个 skill 运行前必须具备以下环境：

- `python3`
- `node`
- 可以访问公开航班页面以及 12306 官方公开接口的网络环境

These dependencies are required both for GitHub usage and for ClawHub / OpenClaw installation.  
无论你是从 GitHub 使用，还是通过 ClawHub / OpenClaw 安装，这些依赖都是必须的。

## Overview | 项目简介

Fly Flight now supports:

- Domestic flights from public Tongcheng flight pages
- High-speed rail from official 12306 public query and public fare endpoints

Fly Flight 当前支持：

- 基于同程公开页面查询国内航班
- 基于 12306 官方公开查询与公开票价接口查询高铁/动车

The skill keeps a single transport entrypoint and routes requests by mode, so one skill can handle both flight and train queries.  
这个 skill 现在使用统一入口，并根据 mode 路由到底层 provider，因此一个 skill 就能同时处理航班和高铁查询。

## What's New in 1.1.0 | 1.1.0 更新内容

- Added a unified `transport_service.py` entrypoint
- Added `train` mode for China high-speed rail lookup
- Kept existing `flight` mode and legacy flight-only entrypoint compatible
- Added sample train query/price data and regression coverage
- Updated skill instructions so OpenClaw can route flight and train requests through the same skill

- 新增统一入口 `transport_service.py`
- 新增 `train` 模式，支持中国高铁/动车查询
- 保留已有 `flight` 模式，并兼容旧的航班单入口脚本
- 新增高铁样例数据与回归测试
- 更新 skill 指令，使 OpenClaw 能在同一个 skill 内路由航班和高铁请求

## Features | 功能特性

- One skill for `flight` and `train`
- One-way and round-trip queries
- City / airport / station / code input support
- Sorting by price, departure, arrival, or duration
- Flight filters: airline, direct-only, preferred airports
- Train filters: train type, seat type, preferred stations
- CLI and local HTTP modes

- 一个 skill 同时支持 `flight` 和 `train`
- 支持单程与往返查询
- 支持城市 / 机场 / 车站 / 代码输入
- 支持按价格、出发时间、到达时间、时长排序
- 航班筛选：航司、直飞、机场偏好
- 高铁筛选：车次类型、席别、车站偏好
- 支持 CLI 和本地 HTTP 服务模式

## Data Sources | 数据来源

Flight mode:

- Tongcheng public flight pages
- `https://www.ly.com/flights/`

Train mode:

- Official 12306 public query endpoints
- `https://kyfw.12306.cn/`

航班模式：

- 同程公开航班页面
- `https://www.ly.com/flights/`

高铁模式：

- 12306 官方公开查询接口
- `https://kyfw.12306.cn/`

## Usage | 使用方式

## Add to OpenClaw | 在 OpenClaw 中添加 Skill

### Install from ClawHub | 从 ClawHub 安装

Before installing, make sure the environment already has `python3` and `node`.  
安装前请先确认运行环境已经具备 `python3` 和 `node`。

If your OpenClaw environment already has ClawHub support, install the skill by slug:

```bash
npx clawhub install fly-flight
```

If needed, install into a specific OpenClaw workspace skills directory:

```bash
npx clawhub install fly-flight --workdir ~/.openclaw/workspace-xiaokui --dir skills
```

如果你的 OpenClaw 环境已经支持 ClawHub，可以直接按 slug 安装：

```bash
npx clawhub install fly-flight
```

如果你要安装到指定的 OpenClaw workspace 的 `skills` 目录，可以这样执行：

```bash
npx clawhub install fly-flight --workdir ~/.openclaw/workspace-xiaokui --dir skills
```

### Install from GitHub | 从 GitHub 手动添加

Before cloning or using the skill, make sure the environment already has `python3` and `node`.  
在克隆或使用这个 skill 之前，请先确认环境已经具备 `python3` 和 `node`。

You can also place this repository directly into the target OpenClaw workspace skill directory:

```bash
cd ~/.openclaw/workspace-xiaokui/skills
git clone https://github.com/baizhexue/fly-flight.git
```

If `fly-flight` already exists, update it in place:

```bash
cd ~/.openclaw/workspace-xiaokui/skills/fly-flight
git pull
```

你也可以把这个仓库直接放进目标 OpenClaw workspace 的 skill 目录：

```bash
cd ~/.openclaw/workspace-xiaokui/skills
git clone https://github.com/baizhexue/fly-flight.git
```

如果已经存在 `fly-flight` 目录，可以直接更新：

```bash
cd ~/.openclaw/workspace-xiaokui/skills/fly-flight
git pull
```

### Reload in OpenClaw | 在 OpenClaw 中重新加载

After adding or updating the skill, reload the target agent or restart the OpenClaw gateway if the old version is still cached.

在添加或更新 skill 之后，如果 OpenClaw 里还显示旧版本，请重新加载对应 agent，或者重启 OpenClaw gateway。

Flight:

```bash
python3 ./scripts/transport_service.py search \
  --mode flight --from 北京 --to 上海 --date 2026-03-20 --sort-by price --pretty
```

High-speed rail:

```bash
python3 ./scripts/transport_service.py search \
  --mode train --from 北京 --to 上海 --date 2026-03-20 \
  --seat-type second_class --sort-by price --pretty
```

Legacy flight-only entrypoint:

```bash
python3 ./scripts/domestic_flight_public_service.py search \
  --from 北京 --to 上海 --date 2026-03-20 --sort-by price --pretty
```

HTTP mode:

```bash
python3 ./scripts/transport_service.py serve --port 8766
```

航班查询：

```bash
python3 ./scripts/transport_service.py search \
  --mode flight --from 北京 --to 上海 --date 2026-03-20 --sort-by price --pretty
```

高铁查询：

```bash
python3 ./scripts/transport_service.py search \
  --mode train --from 北京 --to 上海 --date 2026-03-20 \
  --seat-type second_class --sort-by price --pretty
```

兼容旧版航班入口：

```bash
python3 ./scripts/domestic_flight_public_service.py search \
  --from 北京 --to 上海 --date 2026-03-20 --sort-by price --pretty
```

启动本地 HTTP 服务：

```bash
python3 ./scripts/transport_service.py serve --port 8766
```

## Repository Layout | 仓库结构

- `SKILL.md`: skill instructions and trigger description
- `agents/openai.yaml`: OpenClaw display metadata
- `scripts/transport_service.py`: unified transport CLI and HTTP entrypoint
- `scripts/providers/flight_public_service.py`: flight provider
- `scripts/providers/train_public_service.py`: train provider
- `scripts/domestic_flight_public_service.py`: backward-compatible flight wrapper
- `assets/sample-*.json`: local regression samples

- `SKILL.md`：skill 指令与触发描述
- `agents/openai.yaml`：OpenClaw 展示元数据
- `scripts/transport_service.py`：统一 transport CLI 与 HTTP 入口
- `scripts/providers/flight_public_service.py`：航班 provider
- `scripts/providers/train_public_service.py`：高铁 provider
- `scripts/domestic_flight_public_service.py`：兼容旧版本的航班包装层
- `assets/sample-*.json`：本地回归测试样例数据

## Notes | 说明

- Flight prices are public-page reference prices and may differ from final checkout prices.
- Train prices come from official public fare data; seat availability comes from public query results.
- Public web structures can change, so scraping-based behavior may require maintenance over time.

- 航班价格来自公开页面，仅供参考，可能与最终出票价不同。
- 高铁价格来自官方公开票价数据，余票信息来自公开查询结果。
- 公开网页结构和接口可能变化，因此后续仍可能需要维护。
