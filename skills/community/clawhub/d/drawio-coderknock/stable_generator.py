#!/usr/bin/env python3
"""
Stable Draw.io Flowchart Generator
Creates real draw.io files with actual diagram elements
"""

import os
import sys
from pathlib import Path


class StableFlowGenerator:
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path.cwd()
    
    def generate_ecommerce_architecture(self):
        """Generate e-commerce architecture diagram"""
        title = "电商系统架构图"
        safe_name = "ecommerce_architecture"
        
        drawio_xml = self._generate_architecture_xml(title)
        
        output_file = self.workspace / f"{safe_name}.drawio"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(drawio_xml)
        
        print(f"[OK] Draw.io file generated: {output_file}")
        return output_file
    
    def _generate_architecture_xml(self, title):
        """Generate real draw.io XML with architecture diagram"""
        return f'''<mxfile host="app.diagrams.net">
  <diagram id="architecture" name="{title}">
    <mxGraphModel dx="1178" dy="745" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="1000" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Title -->
        <mxCell id="title" value="{title}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="500" y="10" width="400" height="30" as="geometry" />
        </mxCell>
        
        <!-- User Layer -->
        <mxCell id="user-layer" value="用户层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="1300" height="120" as="geometry" />
        </mxCell>
        
        <mxCell id="web" value="Web浏览器" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="150" y="80" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="mobile" value="移动APP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="320" y="80" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="third" value="第三方应用" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="490" y="80" width="120" height="60" as="geometry" />
        </mxCell>
        
        <!-- Access Layer -->
        <mxCell id="access-layer" value="接入层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="50" y="190" width="1300" height="120" as="geometry" />
        </mxCell>
        
        <mxCell id="cdn" value="CDN/负载均衡" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="150" y="220" width="140" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="waf" value="WAF防火墙" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="340" y="220" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="api" value="API网关" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="510" y="220" width="120" height="60" as="geometry" />
        </mxCell>
        
        <!-- Application Layer -->
        <mxCell id="app-layer" value="应用层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="50" y="330" width="1300" height="200" as="geometry" />
        </mxCell>
        
        <mxCell id="user-svc" value="用户服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="100" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="product-svc" value="商品服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="230" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="order-svc" value="订单服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="360" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="payment-svc" value="支付服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="490" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="inventory-svc" value="库存服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="620" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="search-svc" value="搜索服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="750" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="recommend-svc" value="推荐服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="880" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <!-- Data Layer -->
        <mxCell id="data-layer" value="数据层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="50" y="550" width="1300" height="150" as="geometry" />
        </mxCell>
        
        <mxCell id="user-db" value="用户数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="100" y="580" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="product-db" value="商品数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="230" y="580" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="order-db" value="订单数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="360" y="580" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="payment-db" value="支付数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="490" y="580" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="redis" value="Redis缓存" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="620" y="580" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="es" value="Elasticsearch" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="750" y="580" width="120" height="60" as="geometry" />
        </mxCell>
        
        <!-- Infrastructure Layer -->
        <mxCell id="infra-layer" value="基础设施层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="50" y="720" width="1300" height="120" as="geometry" />
        </mxCell>
        
        <mxCell id="mq" value="消息队列" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="150" y="750" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="log" value="日志系统" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="290" y="750" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="monitor" value="监控系统" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="430" y="750" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="config" value="配置中心" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="570" y="750" width="100" height="60" as="geometry" />
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    
    def find_drawio(self):
        """Find local Draw.io installation"""
        possible_paths = [
            r"C:\Program Files\draw.io\draw.io.exe",
            r"C:\Program Files (x86)\draw.io\draw.io.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def open_drawio(self, drawio_file):
        """Open Draw.io with the generated file"""
        drawio_path = self.find_drawio()
        
        if not drawio_path:
            print("\n[WARN] Draw.io not found")
            print("\n[INSTALL] Download: https://github.com/jgraph/drawio-desktop/releases")
            print("[ONLINE] Or use: https://app.diagrams.net/")
            return False
        
        print(f"\n[OPEN] Starting Draw.io: {drawio_path}")
        print(f"[FILE] Opening: {drawio_file}")
        
        try:
            os.startfile(str(drawio_file))
            print("[OK] Draw.io opened!")
            return True
        except Exception as e:
            print(f"[ERROR] Failed: {e}")
            return False
    
    def run(self, diagram_type="ecommerce"):
        """Run the generator"""
        print("=" * 60)
        print("Stable Draw.io Flowchart Generator")
        print("=" * 60)
        
        if diagram_type == "ecommerce":
            drawio_file = self.generate_ecommerce_architecture()
        else:
            print(f"[ERROR] Unknown diagram type: {diagram_type}")
            return None
        
        self.open_drawio(drawio_file)
        
        print("\n" + "=" * 60)
        print("[DONE] Complete!")
        print("=" * 60)
        
        return drawio_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Stable Draw.io Generator")
    parser.add_argument("--type", "-t", default="ecommerce", help="Diagram type (ecommerce)")
    parser.add_argument("--workspace", "-w", help="Workspace directory")
    
    args = parser.parse_args()
    
    generator = StableFlowGenerator(workspace=args.workspace)
    generator.run(diagram_type=args.type)


if __name__ == "__main__":
    main()
