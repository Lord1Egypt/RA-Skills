#!/usr/bin/env python3
"""
CEX Exchange Architecture Generator
Generates complete CEX exchange architecture diagram
"""

import os
import sys
from pathlib import Path


class CEXArchitectureGenerator:
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path.cwd()
    
    def generate_cex_architecture(self):
        """Generate CEX exchange architecture diagram"""
        title = "CEX 交易所整体架构图"
        safe_name = "cex_exchange_architecture"
        
        drawio_xml = self._generate_cex_xml(title)
        
        output_file = self.workspace / f"{safe_name}.drawio"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(drawio_xml)
        
        print(f"[OK] CEX Architecture Draw.io file generated: {output_file}")
        return output_file
    
    def _generate_cex_xml(self, title):
        """Generate real draw.io XML for CEX exchange architecture"""
        return f'''<mxfile host="app.diagrams.net">
  <diagram id="cex-arch" name="{title}">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Title -->
        <mxCell id="title" value="{title}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=22;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="600" y="10" width="400" height="30" as="geometry" />
        </mxCell>
        
        <!-- User Access Layer -->
        <mxCell id="access-layer" value="用户接入层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="1500" height="120" as="geometry" />
        </mxCell>
        
        <mxCell id="web" value="Web端" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="150" y="80" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="ios" value="iOS APP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="290" y="80" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="android" value="Android APP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="430" y="80" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="api" value="API接口" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="590" y="80" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="websocket" value="WebSocket" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="730" y="80" width="120" height="60" as="geometry" />
        </mxCell>
        
        <!-- Gateway Layer -->
        <mxCell id="gateway-layer" value="网关层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="50" y="190" width="1500" height="120" as="geometry" />
        </mxCell>
        
        <mxCell id="lb" value="负载均衡" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="150" y="220" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="waf" value="WAF/防火墙" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="310" y="220" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="apigw" value="API网关" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="470" y="220" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="ratelimit" value="限流/鉴权" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="610" y="220" width="100" height="60" as="geometry" />
        </mxCell>
        
        <!-- Trading Core Layer -->
        <mxCell id="trading-layer" value="交易核心层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="50" y="330" width="1500" height="180" as="geometry" />
        </mxCell>
        
        <mxCell id="order" value="订单服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="100" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="match" value="撮合引擎" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="240" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="market" value="行情服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="380" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="account" value="账户服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="520" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="asset" value="资产服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="660" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="risk" value="风控服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcccc;strokeColor=#cc0000;" vertex="1" parent="1">
          <mxGeometry x="800" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="liquidation" value="清算服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="940" y="360" width="100" height="60" as="geometry" />
        </mxCell>
        
        <!-- Data Layer -->
        <mxCell id="data-layer" value="数据层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="50" y="530" width="1500" height="150" as="geometry" />
        </mxCell>
        
        <mxCell id="user-db" value="用户数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="100" y="560" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="order-db" value="订单数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="240" y="560" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="asset-db" value="资产数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="380" y="560" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="redis" value="Redis缓存" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="520" y="560" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="kafka" value="Kafka消息" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="660" y="560" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="timeseries" value="时序数据库" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="820" y="560" width="100" height="60" as="geometry" />
        </mxCell>
        
        <!-- Blockchain Layer -->
        <mxCell id="blockchain-layer" value="区块链层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="50" y="700" width="1500" height="140" as="geometry" />
        </mxCell>
        
        <mxCell id="hot-wallet" value="热钱包" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcccc;strokeColor=#cc0000;" vertex="1" parent="1">
          <mxGeometry x="150" y="730" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="cold-wallet" value="冷钱包" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="290" y="730" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="node" value="区块链节点" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="430" y="730" width="120" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="deposit" value="充币服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="590" y="730" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="withdraw" value="提币服务" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="730" y="730" width="100" height="60" as="geometry" />
        </mxCell>
        
        <!-- Ops Layer -->
        <mxCell id="ops-layer" value="运维层" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="50" y="860" width="1500" height="120" as="geometry" />
        </mxCell>
        
        <mxCell id="monitor" value="监控系统" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="150" y="890" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="log" value="日志系统" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="290" y="890" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="backup" value="备份系统" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="430" y="890" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="admin" value="后台管理" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="570" y="890" width="100" height="60" as="geometry" />
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
    
    def run(self):
        """Run the CEX architecture generator"""
        print("=" * 60)
        print("CEX Exchange Architecture Generator")
        print("=" * 60)
        
        drawio_file = self.generate_cex_architecture()
        self.open_drawio(drawio_file)
        
        print("\n" + "=" * 60)
        print("[DONE] CEX Exchange Architecture Complete!")
        print("=" * 60)
        
        return drawio_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="CEX Exchange Architecture Generator")
    parser.add_argument("--workspace", "-w", help="Workspace directory")
    
    args = parser.parse_args()
    
    generator = CEXArchitectureGenerator(workspace=args.workspace)
    generator.run()


if __name__ == "__main__":
    main()
