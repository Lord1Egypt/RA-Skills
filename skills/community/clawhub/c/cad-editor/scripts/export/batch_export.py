"""批量导出工具"""
import os
import glob


class BatchExporter:
    """批量文件处理"""

    @staticmethod
    def batch_dxf_to_png(dxf_dir: str, 
                          output_dir: str,
                          pattern: str = '*.dxf',
                          scale: float = 1.0,
                          dpi: int = 150):
        """
        批量将目录下 DXF 文件转换为 PNG
        
        Args:
            dxf_dir: 源 DXF 目录
            output_dir: 输出目录
            pattern: 文件匹配模式
            scale: 缩放比例
            dpi: 输出分辨率
        Returns:
            成功数量和失败列表
        """
        import ezdxf
        
        os.makedirs(output_dir, exist_ok=True)
        files = glob.glob(os.path.join(dxf_dir, pattern))
        
        success = 0
        failed = []
        
        for fpath in files:
            fname = os.path.basename(fpath)
            name_no_ext = os.path.splitext(fname)[0]
            out_path = os.path.join(output_dir, f'{name_no_ext}.png')
            
            try:
                doc = ezdxf.readfile(fpath)
                render_dxf_to_png(doc, out_path, dpi=dpi)
                success += 1
            except Exception as e:
                failed.append((fname, str(e)))
                
        return {'success': success, 'failed': failed}


def render_dxf_to_png(doc, output_path: str,
                       width: int = 1200,
                       height: int = 900,
                       dpi: int = 150,
                       bg_color: str = 'white'):
    """
    核心渲染函数：DXF文档 → PNG 图片
    
    这是 skill 的"看结果"能力所在——用户不需要CAD软件
    """
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
            dxftype = ent.dxftype()
            if dxftype == 'LINE':
                all_pts.append((ent.dxf.start.x, ent.dxf.start.y))
                all_pts.append((ent.dxf.end.x, ent.dxf.end.y))
            elif dxftype == 'CIRCLE':
                c = (ent.dxf.center.x, ent.dxf.center.y)
                all_pts.append(c); all_pts.append((c[0]+ent.dxf.radius, c[1]+ent.dxf.radius))
            elif dxftype == 'ARC':
                c = (ent.dxf.center.x, ent.dxf.center.y)
                all_pts.append(c); all_pts.append((c[0]+ent.dxf.radius, c[1]+ent.dxf.radius))
            elif dxftype == 'LWPOLYLINE':
                all_pts.extend(list(ent.get_points()))
            elif dxftype in ('TEXT', 'MTEXT'):
                all_pts.append((ent.dxf.insert.x, ent.dxf.insert.y))
        except Exception:
            continue

    if not all_pts:
        fig = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
        plt.axis('off')
        plt.savefig(output_path, dpi=dpi, facecolor=bg_color)
        plt.close(fig)
        return

    xs, ys = [p[0] for p in all_pts], [p[1] for p in all_pts]
    mx, Mx, my, My = min(xs), max(xs), min(ys), max(ys)
    pad = max(Mx - mx, My - my) * 0.1

    fig, ax = plt.subplots(1, 1, figsize=(width/dpi, height/dpi), dpi=dpi)
    ax.set_xlim(mx - pad, Mx + pad)
    ax.set_ylim(my - pad, My + pad)
    ax.set_aspect('equal')
    ax.axis('off')

    # 绘制
    for ent in msp:
        try:
            dt = ent.dxftype()
            cv = _aci_color(getattr(ent.dxf, 'color', 7))
            lw = _lineweight_to_px(getattr(ent.dxf, 'lineweight', 35))

            if dt == 'LINE':
                ax.plot([ent.dxf.start.x, ent.dxf.end.x],
                       [ent.dxf.start.y, ent.dxf.end.y],
                       color=cv, linewidth=lw, solid_capstyle='round')

            elif dt == 'CIRCLE':
                ax.add_patch(plt.Circle(
                    (ent.dxf.center.x, ent.dxf.center.y),
                    ent.dxf.radius, fill=False,
                    edgecolor=cv, linewidth=lw))

            elif dt == 'ARC':
                cx, cy = ent.dxf.center.x, ent.dxf.center.y
                r = ent.dxf.radius
                a1 = np.radians(ent.dxf.start_angle)
                a2 = np.radians(ent.dxf.end_angle)
                t = np.linspace(a1, a2, 60)
                ax.plot(cx + r*np.cos(t), cy + r*np.sin(t), color=cv, linewidth=lw)

            elif dt == 'LWPOLYLINE':
                pts = np.array(list(ent.get_points()))
                if len(pts) > 1:
                    ax.plot(pts[:,0], pts[:,1], color=cv, linewidth=lw,
                           solid_capstyle='round', solid_joinstyle='round')
                    if ent.closed:
                        ax.plot([pts[-1,0],pts[0,0]], [pts[-1,1],pts[0,1]],
                               color=cv, linewidth=lw)

            elif dt == 'TEXT':
                h = ent.dxf.height
                rot = getattr(ent.dxf, 'rotation', 0)
                ax.text(ent.dxf.insert.x, ent.dxf.insert.y,
                       ent.dxf.text or '', fontsize=max(h*3, 6),
                       rotation=rot, color=cv)

            elif dt == 'MTEXT':
                h = getattr(ent, 'char_height', 2.5)
                ins = ent.dxf.insert
                raw_text = ent.text or ''
                text_lines = raw_text.split('\\P') if '\\P' in raw_text else [raw_text]
                for i, line in enumerate(text_lines):
                    ax.text(ins[0], ins[1] - i*h*1.2, line,
                           fontsize=max(h*3, 6), color=cv)

        except Exception:
            continue

    fig.savefig(output_path, dpi=dpi, facecolor=bg_color,
               bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
