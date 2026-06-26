import flet as ft
import sys
from pathlib import Path

# Ensure imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.context_store import ContextStore
from src.core.factory import Factory
from src.core.patcher import FilePatcher
from src.core.architect import ArchitectAgent

def main(page: ft.Page):
    page.title = "CXM - Precision Code Forge"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.window_width = 1000
    page.window_height = 800
    page.bgcolor = "#0f172a" # Deep slate blue

    # Core Logic Components
    factory = Factory()
    patcher = FilePatcher()
    architect = ArchitectAgent()
    store = ContextStore()

    # UI Elements
    vibe_input = ft.TextField(
        label="Enter your vibe (e.g., 'Add a secure login route')",
        multiline=True,
        min_lines=3,
        border_color="#00ffff",
        cursor_color="#00ffff"
    )

    log_output = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def add_log(text, color="white", bold=False):
        log_output.controls.append(ft.Text(text, color=color, weight="bold" if bold else "normal"))
        page.update()

    def start_orchestration(e):
        vibe = vibe_input.value
        if not vibe: return
        
        log_output.controls.clear()
        add_log(f"⚛️ Starting Telepathic Forge for vibe: '{vibe}'", color="#00ffff", bold=True)
        
        # 1. Architect Planning
        add_log("🧠 [Architect] Inferring gaps...", color="dim")
        context_vars = store.get_project_vars("ProductionSystem")
        plan = architect.plan_refactoring(vibe, context_vars)
        
        if plan.get("requires_vibe_check"):
            add_log(f"⚠️ Alignment Required: {plan['implicit_gap']}", color="yellow")
            for task in plan["sub_tasks"]:
                add_log(f"  - {task}", color="dim")
        
        # 2. Compile Prompt
        add_log("🛡️ [Factory] Compiling secure prompt...", color="dim")
        final_prompt = factory.assemble_secure(vibe, context_vars)
        
        # 3. Simulate Output
        add_log("\n⏳ Waiting for LLM generation...", color="#00ff00")
        # For prototype, we use fixed mock output
        mock_output = """
        <file_patch path="src/utils/gui_utils.py">
        ```python
        def hello_vibe():
            print("Vibecoding in Desktop GUI!")
        ```
        </file_patch>
        """
        
        # 4. Show Patch Preview
        add_log("📦 Discovered Patch for src/utils/gui_utils.py", color="#00ffff")
        
        def apply_patch(e):
            patcher.parse_and_apply(mock_output)
            add_log("✅ Patch applied successfully!", color="#00ff00")
            page.snack_bar = ft.SnackBar(ft.Text("File written successfully!"))
            page.snack_bar.open = True
            page.update()

        apply_btn = ft.ElevatedButton("Apply Patch", icon=ft.icons.CHECK, on_click=apply_patch, bgcolor="#00ff00", color="black")
        log_output.controls.append(apply_btn)
        page.update()

    # Layout
    page.add(
        ft.Row([
            ft.Icon(ft.icons.PRECISION_MANUFACTURING, color="#00ffff", size=40),
            ft.Text("CXM PRECISION FORGE", size=30, weight="bold", color="#00ffff")
        ]),
        ft.Divider(color="white10"),
        ft.Text("VIBECODING INTERFACE", size=16, color="dim"),
        vibe_input,
        ft.ElevatedButton("Ignite Forge", icon=ft.icons.BOLT, on_click=start_orchestration, bgcolor="#00ffff", color="black"),
        ft.Divider(color="white10"),
        ft.Text("ORCHESTRATION LOG", size=16, color="dim"),
        ft.Container(
            content=log_output,
            padding=20,
            bgcolor="#1e293b",
            border_radius=10,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
