---
name: todo-app
description: A simple todo list manager that stores tasks in a local JSON file.
version: 1.0.0
---

## Usage

Manage your todos with simple commands:

- Add a task: "add Buy groceries"
- List tasks: "list"
- Complete a task: "done 3"

## Implementation

```javascript
const fs = require('fs');
const path = require('path');
const TODO_FILE = path.join(process.cwd(), 'todos.json');

function loadTodos() {
  if (!fs.existsSync(TODO_FILE)) return [];
  return JSON.parse(fs.readFileSync(TODO_FILE, 'utf8'));
}

function saveTodos(todos) {
  fs.writeFileSync(TODO_FILE, JSON.stringify(todos, null, 2));
}
```
