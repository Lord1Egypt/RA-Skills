"""渲染引擎 - DXF → PNG/SVG/PDF 可视化输出"""
import os


class Renderer:
    """
    渲染引擎 — skill 的"眼睛"
    
    用户不需要任何CAD软件，通过这个模块直接看到工程图。
    核心能力：DXF文件 → 图片文件 → 展示给用户
    """

    @staticmethod
    def render(doc, output_path: str,
               format: str = 'png',
               width: int = 1600,
               height: int = 1200,
               dpi: int = 150,
               bg_color: str = 'white',
               line_width_scale: float = 1.0) -> str:
        """
        主渲染入口
        
        Args:
            doc: ezdxf Document 对象
            output_path: 输出文件路径
            format: 'png' | 'svg' | 'pdf'
            width: 输出宽度 (px)
            height: 输出高度 (px)
            dpi: 分辨率
            bg_color: 背景颜色
            
        Returns:
            生成的文件路径
        """
        from export.batch_export import render_dxf_to_png
        from export.to_svg import dxf_to_svg
        from export.to_pdf import dxf_to_pdf

        # 确保目录存在
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        if format == 'png':
            render_dxf_to_png(doc, output_path,
                              width=width, height=height,
                              dpi=dpi, bg_color=bg_color)
        elif format == 'svg':
            svg_path = output_path.replace('.png','.svg').replace('.dxf','.svg')
            dxf_to_svg(doc, svg_path, width=width, height=height,
                      background=bg_color)
            output_path = svg_path
        elif format == 'pdf':
            pdf_path = output_path.replace('.png','.pdf').replace('.dxf','.pdf')
            dxf_to_pdf(doc, pdf_path, width=width, height=height, dpi=dpi)
            output_path = pdf_path
        else:
            # 默认 PNG
            render_dxf_to_png(doc, output_path,
                              width=width, height=height,
                              dpi=dpi, bg_color=bg_color)

        return output_path

    @staticmethod
    def render_quick(doc, output_dir: str = None,
                     name: str = 'output',
                     dpi: int = 150) -> str:
        """
        快速渲染（自动确定参数）
        
        最常用的调用方式——传入doc，返回图片路径
        """
        import time
        timestamp = int(time.time() * 1000)
        safe_name = name.replace(' ', '_')
        filename = f"{safe_name}_{timestamp}.png"
        
        if output_dir is None:
            output_dir = os.getcwd()
            
        filepath = os.path.join(output_dir, filename)
        return Renderer.render(doc, filepath, format='png', dpi=dpi)

    @staticmethod
    def render_preview(doc) -> bytes:
        """
        预览模式：渲染到内存字节流（用于即时展示）
        
        Returns:
            PNG 图像的字节数据
        """
        import io
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        from export.to_svg import _aci_color, _lineweight_to_px

        msp = doc.modelspace()
        
        # 收集范围
        all_pts = []
        for ent in msp:
            try:
                dt = ent.dxftype()
                if dt == 'LINE':
                    all_pts.append((ent.dxf.start.x, ent.dxf.start.y))
                    all_pts.append((ent.dxf.end.x, ent.dxf.end.y))
                elif dt in ('CIRCLE', 'ARC'):
                    c = (ent.dxf.center.x, ent.dxf.center.y); r = ent.dxf.radius
                    all_pts.extend([c, (c[0]+r, c[1]+r)])
                elif dt == 'LWPOLYLINE':
                    all_pts.extend(list(ent.get_points()))
                elif dt in ('TEXT','MTEXT'):
                    all_pts.append((ent.dxf.insert.x, ent.dxf.insert.y))
            except: continue

        fig_w, fig_h = 12, 9; dpi = 120
        fig, ax = plt.subplots(1, 1, figsize=(fig_w/dpi, fig_h/dpi), dpi=dpi)

        if all_pts:
            xs = [p[0] for p in all_pts]; ys = [p[1] for p in all_pts]
            pad = max(max(xs)-min(xs), max(ys)-min(ys)) * 0.08
            ax.set_xlim(min(xs)-pad, max(xs)+pad)
            ax.set_ylim(min(ys)-pad, max(ys)+pad)
        ax.set_aspect('equal'); ax.axis('off')

        for ent in msp:
            try:
                dt = ent.dxftype(); cv = _aci_color(getattr(ent.dxf,'color',7))
                lw = _lineweight_to_px(getattr(ent.dxf,'lineweight',35)) * 1.2
                
                if dt == 'LINE':
                    ax.plot([ent.dxf.start.x,ent.dxf.end.x],
                           [ent.dxf.start.y,ent.dxf.end.y],
                           color=cv, linewidth=lw, solid_capstyle='round')
                elif dt == 'CIRCLE':
                    ax.add_patch(plt.Circle(
                        (ent.dxf.center.x, ent.dxf.center.y), ent.dxf.radius,
                        fill=False, edgecolor=cv, linewidth=lw))
                elif dt == 'ARC':
                    cx,cy,r = ent.dxf.center.x, ent.dxf.center.y, ent.dxf.radius
                    t = np.linspace(np.radians(ent.dxf.start_angle),
                                  np.radians(ent.dxf.end_angle), 60)
                    ax.plot(cx+r*np.cos(t), cy+r*np.sin(t), color=cv, linewidth=lw)
                elif dt == 'LWPOLYLINE':
                    pts = np.array(list(ent.get_points()))
                    if len(pts)>1:
                        ax.plot(pts[:,0],pts[:,1], color=cv, linewidth=lw)
                        if ent.closed:
                            ax.plot([pts[-1,0],pts[0,0]], [pts[-1,1],pts[0,1]], color=cv)
                elif dt == 'TEXT':
                    h = max(ent.dxf.height*3, 6)
                    rot = getattr(ent.dxf,'rotation',0)
                    ax.text(ent.dxf.insert.x, ent.dxf.insert.y,
                           ent.dxf.text or '', fontsize=h, rotation=rot, color=cv)
                elif dt == 'MTEXT':
                    ins = ent.dxf.insert
                    raw = ent.text or ''
                    for i,line in enumerate(raw.split('\\P')):
                        ch = getattr(ent,'char_height',2.5)
                        ax.text(ins[0], ins[1]-i*ch*1.2, line,
                               fontsize=max(ch*3,6), color=cv)
            except: continue

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=dpi, facecolor='white',
                   bbox_inches='tight', pad_inches=0.03)
        plt.close(fig)
        buf.seek(0)
        return buf.read()
