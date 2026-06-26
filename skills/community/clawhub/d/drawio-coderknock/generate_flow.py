#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draw.io 流程图生成器
根据用户描述自动生成流程图，检测本地 Draw.io 并自动打开
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class DrawioFlowGenerator:
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path.cwd()
        self.templates_dir = Path(__file__).parent / "templates"
        self.ensure_templates()
    
    def ensure_templates(self):
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True)
            self.create_default_templates()
    
    def create_default_templates(self):
        templates = {
            "login_flow": """flowchart TD
    Start([开始]) --> Input[用户输入信息]
    Input --> Validate{验证输入?}
    Validate -->|通过| CheckDB{验证凭据?}
    CheckDB -->|成功| Success[登录成功]
    Success --> End([结束])
    Validate -->|失败| Err1[提示错误]
    Err1 --> Input
    CheckDB -->|失败| Err2[提示错误]
    Err2 --> Input""",
            
            "order_flow": """flowchart TD
    Start([开始]) --> Create[创建订单]
    Create --> CheckStock{检查库存?}
    CheckStock -->|有货| Payment[支付处理]
    Payment --> PaySuccess{支付成功?}
    PaySuccess -->|是| Ship[发货]
    Ship --> Complete[订单完成]
    Complete --> End([结束])
    CheckStock -->|缺货| NoStock[通知缺货]
    NoStock --> End
    PaySuccess -->|否| PayFail[支付失败]
    PayFail --> End""",
            
            "approval_flow": """flowchart TD
    Start([开始]) --> Submit[提交申请]
    Submit --> Review1[一级审批]
    Review1 --> Approve1{批准?}
    Approve1 -->|是| Review2[二级审批]
    Approve1 -->|否| Reject[拒绝]
    Review2 --> Approve2{批准?}
    Approve2 -->|是| Approve[批准通过]
    Approve2 -->|否| Reject
    Approve --> End([结束])
    Reject --> Notify[通知申请人]
    Notify --> End""",
            
            "generic_flow": """flowchart TD
    Start([开始]) --> Step1[第一步]
    Step1 --> Step2[第二步]
    Step2 --> Decision{判断?}
    Decision -->|是| PathA[路径A]
    Decision -->|否| PathB[路径B]
    PathA --> End([结束])
    PathB --> End"""
        }
        
        for name, content in templates.items():
            with open(self.templates_dir / f"{name}.mmd", "w", encoding="utf-8") as f:
                f.write(content)
    
    def find_drawio(self):
        possible_paths = []
        
        if sys.platform == "win32":
            possible_paths = [
                r"C:\Program Files\draw.io\draw.io.exe",
                r"C:\Program Files (x86)\draw.io\draw.io.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Programs\draw.io\draw.io.exe"),
            ]
        elif sys.platform == "darwin":
            possible_paths = [
                "/Applications/draw.io.app/Contents/MacOS/draw.io",
            ]
        else:
            possible_paths = [
                "/usr/bin/drawio",
                "/usr/local/bin/drawio",
                "/snap/bin/drawio",
            ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        try:
            if sys.platform == "win32":
                result = subprocess.run(["where", "draw.io"], capture_output=True, text=True)
            else:
                result = subprocess.run(["which", "drawio"], capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def generate_drawio_xml(self, mermaid_code, title="流程图"):
        escaped_code = mermaid_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f"""<mxfile host="app.diagrams.net">
  <diagram id="flow-diagram" name="{title}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="note" value="Use: Arrange -&gt; Insert -&gt; Advanced -&gt; Mermaid&amp;#xa;&amp;#xa;{escaped_code}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="900" height="600" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    
    def generate_flow(self, description, template_type="generic"):
        print(f"[GENERATE] Generating flowchart: {description}")
        
        template_map = {
            "登录": "login_flow",
            "注册": "login_flow",
            "订单": "order_flow",
            "支付": "order_flow",
            "审批": "approval_flow",
            "审核": "approval_flow",
        }
        
        selected_template = "generic_flow"
        for keyword, template in template_map.items():
            if keyword in description:
                selected_template = template
                break
        
        if template_type and template_type != "generic":
            selected_template = template_type
        
        template_file = self.templates_dir / f"{selected_template}.mmd"
        if template_file.exists():
            with open(template_file, "r", encoding="utf-8") as f:
                mermaid_code = f.read()
        else:
            template_file = self.templates_dir / "generic_flow.mmd"
            with open(template_file, "r", encoding="utf-8") as f:
                mermaid_code = f.read()
        
        safe_name = description.replace(" ", "_").replace("/", "_").replace("\\", "_")[:50]
        output_file = self.workspace / f"{safe_name}.drawio"
        mmd_file = self.workspace / f"{safe_name}.mmd"
        
        with open(mmd_file, "w", encoding="utf-8") as f:
            f.write(mermaid_code)
        print(f"[OK] Mermaid saved: {mmd_file}")
        
        drawio_xml = self.generate_drawio_xml(mermaid_code, title=description)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(drawio_xml)
        print(f"[OK] Draw.io file generated: {output_file}")
        
        return output_file, mmd_file, mermaid_code
    
    def open_drawio(self, drawio_file):
        drawio_path = self.find_drawio()
        
        if not drawio_path:
            print("\n[WARN] Draw.io not found")
            print("\n[INSTALL] Please install Draw.io:")
            print("   Download: https://github.com/jgraph/drawio-desktop/releases")
            if sys.platform == "win32":
                print("   Or run: winget install drawio")
            elif sys.platform == "darwin":
                print("   Or run: brew install --cask drawio")
            print("\n[ONLINE] Or use: https://app.diagrams.net/")
            return False
        
        print(f"\n[OPEN] Starting Draw.io: {drawio_path}")
        print(f"[FILE] Opening: {drawio_file}")
        
        try:
            if sys.platform == "win32":
                os.startfile(str(drawio_file))
            elif sys.platform == "darwin":
                subprocess.run(["open", str(drawio_file)])
            else:
                subprocess.run([drawio_path, str(drawio_file)])
            return True
        except Exception as e:
            print(f"[ERROR] Failed to open: {e}")
            return False
    
    def run(self, description, template_type=None):
        print("=" * 60)
        print("Draw.io Flowchart Generator")
        print("=" * 60)
        
        drawio_file, mmd_file, mermaid_code = self.generate_flow(description, template_type)
        
        print("\n" + "=" * 60)
        print("Mermaid Code:")
        print("=" * 60)
        print(mermaid_code)
        print("=" * 60)
        
        self.open_drawio(drawio_file)
        
        print("\n[DONE] Complete!")
        print(f"   Draw.io: {drawio_file}")
        print(f"   Mermaid: {mmd_file}")
        print("\n[TIP] In Draw.io use: Arrange -> Insert -> Advanced -> Mermaid")
        print("   Paste the Mermaid code to generate full flowchart!")
        
        return drawio_file


def main():
    parser = argparse.ArgumentParser(description="Draw.io Flowchart Generator")
    parser.add_argument("description", nargs="?", help="Flowchart description, e.g. 'User Login'")
    parser.add_argument("--template", "-t", help="Template type (login|order|approval|generic)")
    parser.add_argument("--test", action="store_true", help="Test mode")
    parser.add_argument("--workspace", "-w", help="Workspace directory")
    
    args = parser.parse_args()
    
    if args.test:
        print("[TEST] Test mode - generating test flowchart")
        generator = DrawioFlowGenerator(workspace=args.workspace)
        generator.run("Test Flow", template_type="generic")
        return
    
    if not args.description:
        print("Usage: python generate_flow.py 'flowchart description'")
        print("\nExamples:")
        print("  python generate_flow.py 'User Login'")
        print("  python generate_flow.py 'Order Process' --template order")
        print("  python generate_flow.py 'Approval Flow' --template approval")
        return
    
    generator = DrawioFlowGenerator(workspace=args.workspace)
    generator.run(args.description, template_type=args.template)


if __name__ == "__main__":
    main()
