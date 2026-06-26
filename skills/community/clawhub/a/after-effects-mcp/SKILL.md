---
name: after-effects-mcp
description: Automates Adobe After Effects using ExtendScript (.jsx) files and aerender CLI. Supports composition creation, effect application, batch rendering, project templates, and Adobe Media Encoder workflows.
---

# After Effects MCP Bridge

This skill enables programmatic control of Adobe After Effects via ExtendScript (.jsx) automation and command-line tools.

## 🛠️ Core Capabilities

### 1. ExtendScript Automation
Use `scripts/ae_script.jsx` to execute After Effects operations:
- Create/modify compositions
- Add layers, effects, keyframes
- Batch render projects
- Manipulate project structure

### 2. Command-Line Rendering
Use `aerender` (After Effects command-line renderer) for:
- Headless rendering
- Batch processing
- Queue management

### 3. Project Template System
Use `assets/templates/` for reusable AE project templates.

---

## 📋 Usage Patterns

### Pattern 1: Create Composition Programmatically

```jsx
// scripts/create_comp.jsx
var comp = app.project.items.addComp("MyComp", 1920, 1080, 1, 30, 300);
var solid = comp.layers.addSolid([1,0,0], "Red Solid", 1920, 1080, 1);
```

### Pattern 2: Batch Render Project

```bash
aerender -project ./my_project.aep -output ./output.mov -mp
```

### Pattern 3: Apply Effect via Script

```jsx
// scripts/apply_effect.jsx
var layer = app.project.activeItem.selectedLayer(1);
layer.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur");
```

---

## 🔧 Available Scripts

| Script | Purpose |
|--------|---------|
| `create_comp.jsx` | Create new composition with specified params |
| `batch_render.jsx` | Queue multiple compositions for render |
| `apply_effect.jsx` | Apply effects to selected layers |
| `export_template.jsx` | Save project as template (.aet) |

---

## 🚀 Quick Start Workflow

1. **Check AE Installation**: Verify After Effects is installed
   ```bash
   which aerender
   ```

2. **Load Project**: Open existing .aep or create new
   ```jsx
   app.open(new File("./my_project.aep"));
   ```

3. **Execute Script**: Run ExtendScript via:
   - AE: File → Scripts → Run Script File
   - Command-line: `aerender -script ./myscript.jsx`

4. **Render Output**: Use aerender for headless rendering

---

## ⚠️ Requirements

- Adobe After Effects installed (CC 2019+)
- ExtendScript Toolkit (optional, for debugging)
- aerender in PATH for command-line rendering

---

## 📚 References

- **ExtendScript Guide**: See `references/extendscript_api.md`
- **Effect Names**: See `references/effect_names.md`
- **Render Settings**: See `references/render_settings.md`

---

## 🎯 Monitoring

Be verbose about:
- Composition settings (resolution, duration, framerate)
- Effect choices and parameters
- Render queue status
- Output format decisions
