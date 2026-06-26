# Desktop AI Agent Skill

Use this skill when the user wants to:
- Control desktop applications
- Teach the AI to perform tasks
- Have the AI learn from demonstrations
- Automate desktop workflows

## Commands

### Take Screenshot
```python
from desktop_agent import get_agent
agent = get_agent()
agent.capture_to_file("screenshot.png")
```

### Get Mouse Position
```python
agent = get_agent()
pos = agent.get_mouse_position()  # Returns (x, y)
```

### Mouse Control
```python
agent = get_agent()
agent.move_to(x, y)           # Move mouse
agent.click(x, y)             # Click
agent.double_click(x, y)      # Double click  
agent.right_click(x, y)      # Right click
agent.drag_to(x, y)           # Drag
```

### Keyboard Control
```python
agent = get_agent()
agent.type("Hello world")     # Type text
agent.press("enter")           # Press key
agent.hotkey("ctrl", "c")     # Ctrl+C
```

### Teaching Mode
```python
from desktop_agent import get_agent
from desktop_agent.teacher import TaskTeacher

agent = get_agent()
teacher = TaskTeacher(agent)

# Start teaching
teacher.start_teaching("my_task")

# Record actions
teacher.record_click()        # Records current mouse position
teacher.record_click(100, 200) # Records specific position
teacher.record_type("text")
teacher.record_press("enter")
teacher.record_hotkey("ctrl", "s")
teacher.record_wait(2)        # Wait 2 seconds

# Show steps
teacher.show_steps()

# Save or cancel
teacher.finish_teaching()
teacher.cancel_teaching()
```

### Running Learned Tasks
```python
agent = get_agent()
tasks = agent.list_tasks()    # List all tasks
agent.execute_task("task_name") # Run a task
```

## Files

- `desktop_agent/__init__.py` - Core agent
- `desktop_agent/teacher.py` - Teaching system  
- `learned_tasks/` - Saved task definitions

## Notes

- AI can see screen and control mouse/keyboard
- User can teach by demonstration
- Tasks are saved as JSON and reusable
- Use with caution - can control any application
