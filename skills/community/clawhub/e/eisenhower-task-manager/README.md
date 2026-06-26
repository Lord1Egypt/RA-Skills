# Eisenhower Task Manager

A comprehensive task management system built around the Eisenhower Matrix methodology, featuring customer project tracking, delegation lists, and a powerful real-time web dashboard.

## 🚀 The Dashboard

The crown jewel of this skill is its interactive, real-time web dashboard. It provides a visual, drag-and-drop interface for all your tasks, automatically staying in sync with your local markdown files.

### 💻 Integrated Terminal & AI Sync
- **Built-in Shell**: A fully functional, resizable web terminal integrated directly into the dashboard.
- **Smart Detection**: Automatically detects and uses your default login shell (e.g., `zsh` or `bash`).
- **Persistent Sessions**: The terminal process runs in the background. If you refresh the page, your terminal history and running processes remain exactly as you left them.
- **VS Code Shortcuts**: Use `Ctrl + \`` or `Cmd + J` to quickly toggle the terminal panel from anywhere in the dashboard.
- **Customizable Layout**: Drag the resizer to adjust height, or double-click the terminal header to instantly maximize it to full screen.
- **AI Agent Integration**: Start your code agent (like Trae or Claude Code) inside the terminal and chat in natural language to add tasks, manage projects, and sync with external systems using special rules—all without leaving the dashboard.

### 📋 Task Management Operations
The dashboard isn't just for viewing; it's a fully interactive task manager:

- **Quick Actions**: Hover over any task to reveal action buttons.
- **Drag and Drop**: Drag tasks to quickly reorder them or move them between quadrants.
- **Move Tasks**: Click the move icon (→) to open a contextual menu to move a task to another list (e.g., from a Quadrant to the Maybe or Delegation list).
- **Complete Tasks**: Mark tasks as complete with a single click. They are automatically moved to your `archived.md` file.
- **Copy Tasks**: Click the copy icon (⎘) to copy a task to another list (e.g., from a Quadrant to a Customer Project, or to the Delegation list) without removing the original.
- **Delete Tasks**: Remove obsolete tasks cleanly.
- **Real-time Sync**: Every action taken in the dashboard instantly updates the underlying markdown files, and any changes made directly to the markdown files (e.g., via CLI or IDE) instantly reflect in the dashboard via WebSockets.

### 📊 Views & Analytics
- **Four-Quadrant Matrix**: Visual layout of Q1 (Urgent/Important) through Q4.
- **Customer Projects**: Dedicated view for tracking long-term client engagements.
- **Delegation Tracker**: Monitor tasks you've assigned to others, filtering by "In Progress" or "Overdue".
- **Maybe List**: A parking lot for ideas and future considerations.
- **Live Statistics**: Real-time counters showing task distribution across all quadrants and lists.

## 🛠 Getting Started

### Starting the Dashboard
You can start the dashboard in the background (daemon mode) so it survives terminal closures:

```bash
cd dashboard
./start.sh --daemon
```

*To stop the daemon later, simply run `./stop.sh`.*

### Task Directory Configuration
By default, tasks are stored in the `tasks/` directory. You can override this globally by setting an environment variable:
```bash
export EISENHOWER_TASKS_DIR=/path/to/your/custom/tasks
```

## 🧠 Core Philosophy
1. **Customer projects NEVER duplicate** - exist only in Customer Project List unless they require *your immediate personal execution*.
2. **Sequential numbering** - Tasks are strictly numbered without gaps.
3. **Markdown-First** - Your data is portable, human-readable, and never locked into a proprietary database.
