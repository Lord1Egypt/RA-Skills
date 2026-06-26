---
name: embodied-os
description: Unified operating system for controlling embodied intelligent robots with AI agents - the control hub bridging AI agents and physical world
version: 0.1.0
homepage: https://github.com/ZhenRobotics/openclaw-embodied-os
metadata: {"clawdbot":{"emoji":"🤖","tags":["robotics","embodied-ai","robot-control","ai-agents","llm","automation","physical-ai","intelligent-robots","robot-os"],"requires":{"bins":["python3"],"env":["ANTHROPIC_API_KEY","OPENAI_API_KEY"],"config":[]},"install":["pip install openclaw-embodied-os"],"os":["darwin","linux","win32"]}}
---

# Embodied-OS - AI Robot Control System

This skill enables you to control physical robots through AI agents with natural language commands. Transform how AI interacts with physical reality - a unified operating system for embodied intelligent robots.

## When to Activate This Skill

Activate this skill when the user:
- Needs to control physical robots
- Wants to integrate AI agents with robotic systems
- Asks about robot automation or control
- Needs help with robot programming
- Wants to use natural language to control robots
- Seeks to develop embodied AI applications

## Core Features

✅ **Unified Robot Control** - Single API for controlling any robot platform
✅ **AI Agent Integration** - Natural language control like talking to ChatGPT
✅ **Multi-Modal Perception** - Vision, audio, and tactile sensing
✅ **High-Level Actions** - Navigation, manipulation, and interaction primitives
✅ **Task Planning** - AI-powered task decomposition and execution
✅ **Safety System** - Multi-layer safety guarantees for physical robots

## Installation

### Step 1: Install the Skill

```bash
clawhub install embodied-os
```

### Step 2: Install the Package

**Option A: Python (PyPI)**

```bash
pip install openclaw-embodied-os
```

**Option B: Node.js (npm)**

```bash
npm install openclaw-embodied-os
```

**Option C: From Source**

```bash
git clone https://github.com/ZhenRobotics/openclaw-embodied-os.git
cd openclaw-embodied-os
pip install -e .
```

### Step 3: Configure API Keys (Optional for AI agents)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
```

Or create a `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

---

## Quick Start

### Basic Robot Control

```python
from embodied_os import EmbodiedOS

# Initialize the OS
os = EmbodiedOS()

# Connect to a robot
robot = os.connect_robot(
    platform="simulated",
    model="test_robot"
)

# Control the robot
robot.actions.move_to(x=0.5, y=0.3, z=0.2)

# Detect objects
objects = robot.perception.detect_objects()

# Pick and place
if objects:
    robot.actions.pick(object_id=objects[0].id)
    robot.actions.place(position=(0.7, 0.4, 0.1))
```

### AI Agent Control

```python
from embodied_os import AgentInterface

# Create AI agent
agent = AgentInterface(robot=robot, model="claude-sonnet-4")

# Natural language control
agent.execute("Pick up the red cube and place it in the box")

# Conversation
response = agent.chat("What do you see?")
print(response)
```

---

## Supported Robot Platforms

### Current Support
- **Universal Robots** (UR3e, UR5e, UR10e)
- **Franka Emika** Panda
- **Boston Dynamics** Spot
- **Simulated Robots** (for testing)

### Coming Soon
- ABB robots
- KUKA robots
- Custom robots via plugin system

---

## Use Cases

### 1. Warehouse Automation
```python
warehouse_robot = os.connect_robot(platform="mobile_manipulator")

agent.execute("""
    Go to aisle 5, shelf B.
    Pick up all items marked with red tags.
    Transport them to the packing station.
    Report the quantity and item IDs.
""")
```

### 2. Elderly Care Assistant
```python
care_robot = os.connect_robot(platform="service_robot")

agent.monitor_and_assist("""
    Watch for the person calling for help.
    If they ask for water, bring them a glass.
    If they drop something, pick it up.
""")
```

### 3. Research Lab Assistant
```python
lab_robot = os.connect_robot(platform="dual_arm_robot")

agent.execute("""
    Set up the chemistry experiment:
    1. Measure 50ml of solution A
    2. Heat to 60 degrees
    3. Add catalyst
    4. Stir for 2 minutes
""")
```

---

## Core Capabilities

### 1. Unified Robot Control Interface
- Single API for controlling any robot
- Works across different platforms and manufacturers
- Plug-and-play integration

### 2. AI Agent Natural Language Control
- Control robots like talking to ChatGPT
- Supports Claude, GPT, and custom agents
- Context-aware task execution

### 3. Multi-Modal Perception
- **Vision**: Camera, object detection, depth sensing
- **Audio**: Sound capture, speech recognition
- **Tactile**: Force sensors, contact detection

### 4. High-Level Action Primitives

```python
# Navigation
robot.actions.navigate_to(x=2.0, y=1.5, theta=0)

# Manipulation
robot.actions.pick(object="cup")
robot.actions.place(location="table")

# Interaction
robot.actions.press_button(target="elevator")
robot.actions.open_door(handle_position=[1.0, 0.5, 1.0])
```

### 5. AI-Powered Task Planning

```python
# High-level task
task = "Prepare coffee for the user"

# Automatic decomposition and execution
plan = robot.planner.create_plan(task)
robot.planner.execute(plan, monitor=True)
```

### 6. Multi-Layer Safety System

```python
# Define safety constraints
robot.safety.set_workspace_bounds(
    x_min=0, x_max=2.0,
    y_min=-1.0, y_max=1.0,
    z_min=0, z_max=1.5
)

# Force limits
robot.safety.set_max_force(50.0)

# Collision avoidance
robot.safety.enable_collision_avoidance()
```

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              AI Agent Layer                     │
│         (Claude, GPT, Custom Agents)            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│            Embodied-OS Core                     │
│  ┌─────────┐  ┌─────────┐  ┌────────────┐     │
│  │ Natural │  │  Task   │  │   Safety   │     │
│  │Language │  │ Planner │  │ Validator  │     │
│  └─────────┘  └─────────┘  └────────────┘     │
│  ┌─────────┐  ┌─────────┐  ┌────────────┐     │
│  │Perception│  │ Action  │  │   State    │     │
│  │ Module  │  │Executor │  │  Manager   │     │
│  └─────────┘  └─────────┘  └────────────┘     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      Robot Abstraction Layer (RAL)              │
│   Unified interface for all robot types         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│           Physical Robots                       │
│  Manipulators | Mobile | Humanoids | Drones    │
└─────────────────────────────────────────────────┘
```

---

## Configuration

Create a `config.yaml` file:

```yaml
robot:
  platform: universal_robot
  model: UR5e
  endpoint: 192.168.1.100

perception:
  cameras:
    - name: head_camera
      type: realsense_d435
      resolution: [1280, 720]
      fps: 30

safety:
  workspace:
    x: [0, 2.0]
    y: [-1.0, 1.0]
    z: [0, 1.5]
  max_velocity: 0.5  # m/s
  max_force: 50  # N

agent:
  model: claude-sonnet-4
  api_key: ${ANTHROPIC_API_KEY}
```

---

## API Reference

### Core Classes

#### `EmbodiedOS`
Main interface to the system.

```python
os = EmbodiedOS(config_path="config.yaml")
robot = os.connect_robot(platform, model, endpoint)
os.disconnect_all()
```

#### `Robot`
Represents a connected robot.

```python
robot.actions.move_to(x, y, z)
robot.perception.get_image()
robot.state.get_joint_positions()
robot.safety.emergency_stop()
```

#### `AgentInterface`
AI agent control interface.

```python
agent = AgentInterface(model="claude-4", robot=robot)
agent.execute(task_description)
agent.chat(message)
```

---

## Requirements

- **Python**: 3.9 or higher
- **Dependencies**: numpy>=1.20.0, pyyaml>=6.0
- **Optional**: ROS2 (for ROS integration)
- **Optional**: CUDA (for vision processing)
- **Optional**: Anthropic API key (for Claude agent)
- **Optional**: OpenAI API key (for GPT agent)

---

## Examples

See the `examples/` directory:
- `basic_control.py` - Basic robot control
- `agent_control.py` - AI agent interaction

Run examples:
```bash
python examples/basic_control.py
python examples/agent_control.py
```

---

## Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-embodied-os
- **npm**: https://www.npmjs.com/package/openclaw-embodied-os
- **PyPI**: https://pypi.org/project/openclaw-embodied-os/
- **README**: Complete documentation and guides
- **QUICKSTART**: 5-minute quick start guide

---

## Roadmap

### Phase 1: Core Platform (Current)
- [x] Robot abstraction layer
- [x] Basic perception system
- [x] Action executor
- [x] Safety system
- [x] Agent interface

### Phase 2: Advanced Features (Q2 2026)
- [ ] Multi-robot coordination
- [ ] Advanced vision processing
- [ ] Learning from demonstration
- [ ] Cloud deployment

### Phase 3: Ecosystem (Q3 2026)
- [ ] Skill marketplace
- [ ] Community plugins
- [ ] Simulation environments
- [ ] Mobile app control

---

## License

MIT License - see LICENSE file for details.

---

## Changelog

### v0.1.0 (2026-03-08)
- Initial release
- Unified robot control interface across platforms
- AI Agent natural language control
- Multi-modal perception (vision, audio, tactile)
- High-level action primitives
- AI-powered task planning
- Multi-layer safety system
- Support for Universal Robots, Franka Panda, Boston Dynamics Spot
- Simulated robot support for testing

---

## Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-embodied-os
- **npm**: https://www.npmjs.com/package/openclaw-embodied-os
- **PyPI**: https://pypi.org/project/openclaw-embodied-os/
- **Release**: https://github.com/ZhenRobotics/openclaw-embodied-os/releases/tag/v0.1.0

---

**Embodied-OS - Making robots as easy to control as talking to a friend.**
