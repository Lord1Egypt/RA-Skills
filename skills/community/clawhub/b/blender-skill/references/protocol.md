# Communication Protocol

TCP 9876 request and response shape, plus the two code patterns used most often. `result` must be a dict.

## Communication Protocol

### TCP Socket Protocol

**Request format** (null-byte delimited JSON):
```json
{"type": "execute", "code": "import bpy\nresult = {'key': 'value'}", "strict_json": false}\0
```

**Response format**:
```json
// Success
{"status": "ok", "result": {"key": "value"}, "stdout": "", "stderr": ""}\0

// Error
{"status": "error", "message": "Traceback...", "stdout": "", "stderr": ""}\0
```

### Code Execution Conventions

- Assign return value to the `result` variable (must be a dict)
- `strict_json=True`: strict JSON serialization; non-serializable values will error
- `strict_json=False`: uses `repr()` as fallback for non-JSON values
- Supports deferred responses: return a `check_is_finished` callable for long-running tasks

### Example: Get Object Info

```python
import bpy
obj = bpy.data.objects.get("Cube")
if obj:
    result = {
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "vertices": len(obj.data.vertices) if obj.type == "MESH" else 0,
    }
else:
    result = {"error": "Object not found"}
```

### Example: Create an Object

```python
import bpy
bpy.ops.mesh.primitive_torus_add(
    align='WORLD',
    location=(0, 0, 0),
    major_radius=1.0,
    minor_radius=0.3,
)
result = {"status": "created", "name": bpy.context.active_object.name}
```

---
