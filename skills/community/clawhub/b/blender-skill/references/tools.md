# Built-in Tools

Moved out of SKILL.md so the skill entry stays inside the scanner's per-file budget. The tool names and parameters below are the official Blender MCP server surface (add-on v1.0.3).

## Built-in Tools (20 total)

### Core
| Tool | Description | Params |
|------|-------------|--------|
| `execute_blender_code` | Execute arbitrary Python code (full bpy access) | `code: str` |
| `execute_blender_code_for_cli` | Execute code in a background Blender process | `blend_file: str, code: str` |

### Scene Analysis
| Tool | Description | Params |
|------|-------------|--------|
| `get_objects_summary` | Get scene object hierarchy and basic info | none |
| `get_object_detail_summary` | Get detailed info for a specific object | `object_name: str` |
| `get_blendfile_summary_datablocks` | Analyze .blend file data-blocks | `blend_file: str` |
| `get_blendfile_summary_missing_files` | Check for missing external file references | `blend_file: str` |
| `get_blendfile_summary_of_linked_libraries` | List linked external libraries | `blend_file: str` |
| `get_blendfile_summary_path_info` | Analyze .blend file path information | `blend_file: str` |
| `get_blendfile_summary_usage_guess` | Guess the purpose of a .blend file | `blend_file: str` |

### Screenshots & Rendering
| Tool | Description | Params |
|------|-------------|--------|
| `get_screenshot_of_window_as_image` | Capture Blender window screenshot | none |
| `get_screenshot_of_area_as_image` | Capture specific area screenshot | `area_type: str` |
| `get_screenshot_of_window_as_json` | Get window layout as JSON description | none |
| `render_viewport_to_path` | Render viewport to file | `output_path: str` |
| `render_thumbnail_to_path` | Render thumbnail to file | `output_path: str` |

### Navigation
| Tool | Description | Params |
|------|-------------|--------|
| `jump_to_tab_by_name` | Jump to a named editor tab | `tab_name: str` |
| `jump_to_tab_by_space_type` | Jump to a space type | `space_type: str` |
| `jump_to_view3d_object_by_name` | Focus on an object in 3D View | `object_name: str` |
| `jump_to_view3d_object_data_by_name` | Focus on object data in 3D View | `data_name: str` |

### Documentation Search
| Tool | Description | Params |
|------|-------------|--------|
| `search_api_docs` | Search Blender Python API docs | `query: str` |
| `search_manual_docs` | Search Blender user manual | `query: str` |
| `get_python_api_docs` | Get Python API docs | `query: str` |

---
