"""DXF → SVG 矢量导出"""
import ezdxf


def dxf_to_svg(doc, output_path: str,
               width: int = 800,
               height: int = 600,
               background: str = 'white',
               filter_layers: list = None):
    """
    将 DXF 文档渲染为 SVG 文件
    
    Args:
        doc: ezdxf Document
        output_path: 输出文件路径
        width: SVG 宽度 (px)
        height: SVG 高度 (px)
        background: 背景色
        filter_layers: 只导出指定图层（None=全部）
    """
    import io

    try:
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addon.drawing.matplotlib import MatplotlibBackend
        import matplotlib.pyplot as plt
        
        fig = plt.figure(figsize=(width/100, height/100), dpi=100)
        ax = fig.add_axes([0, 0, 1, 0])
        
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        
        Frontend(ctx, out).draw_layout(
            doc.modelspace(),
            finalize=True
        )
        
        fig.savefig(output_path, format='svg', dpi=100,
                   facecolor=background, edgecolor='none')
        plt.close(fig)
        
    except ImportError:
        # Fallback: 用 matplotlib 直接绘制
        _dxf_to_svg_fallback(doc, output_path, width, height)


def _dxf_to_svg_fallback(doc, output_path: str, width=800, height=600):
    """备用SVG导出（纯matplotlib，不依赖ezdxf的drawing addon）"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    # 收集所有实体范围
    all_pts = []
    for entity in doc.modelspace():
        try:
            if entity.dxftype() == 'LINE':
                all_pts.append((entity.dxf.start.x, entity.dxf.start.y))
                all_pts.append((entity.dxf.end.x, entity.dxf.end.y))
            elif entity.dxftype() in ('CIRCLE', 'ARC'):
                all_pts.append((entity.dxf.center.x, entity.dxf.center.y))
                r = entity.dxf.radius
                all_pts.append((entity.dxf.center.x + r, entity.dxf.center.y + r))
                all_pts.append((entity.dxf.center.x - r, entity.dxf.center.y - r))
            elif entity.dxftype() == 'LWPOLYLINE':
                pts = list(entity.get_points())
                for p in pts:
                    all_pts.append(p[:2])
            elif entity.dxftype() == 'TEXT' or entity.dxftype() == 'MTEXT':
                ins = entity.dxf.insert
                all_pts.append((ins[0], ins[1]))
        except Exception:
            continue
    
    if not all_pts:
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.savefig(output_path, format='svg')
        plt.close()
        return

    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    
    margin_x = max(xs) - min(xs)
    margin_y = max(ys) - min(ys)
    pad_x = margin_x * 0.05 if margin_x > 0 else 10
    pad_y = margin_y * 0.05 if margin_y > 0 else 10
    
    fig, ax = plt.subplots(1, 1, figsize=(width/100, height/100), dpi=100)
    ax.set_xlim(min(xs)-pad_x, max(xs)+pad_x)
    ax.set_ylim(min(ys)-pad_y, max(ys)+pad_y)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 绘制所有图元
    for entity in doc.modelspace():
        try:
            color_val = getattr(entity.dxf, 'color', 7)
            
            if entity.dxftype() == 'LINE':
                sx, sy = entity.dxf.start.x, entity.dxf.start.y
                ex, ey = entity.dxf.end.x, entity.dxf.end.y
                ax.plot([sx, ex], [sy, ey], color=_aci_color(color_val),
                       linewidth=_lineweight_to_px(getattr(entity.dxf, 'lineweight', 35)))
                       
            elif entity.dxftype() == 'CIRCLE':
                cx, cy = entity.dxf.center.x, entity.dxf.center.y
                r = entity.dxf.radius
                circle = plt.Circle((cx, cy), r, fill=False,
                                    edgecolor=_aci_color(color_val),
                                    linewidth=_lineweight_to_px(getattr(entity.dxf, 'lineweight', 35)))
                ax.add_patch(circle)

            elif entity.dxftype() == 'ARC':
                cx, cy = entity.dxf.center.x, entity.dxf.center.y
                r = entity.dxf.radius
                a1 = np.radians(entity.dxf.start_angle)
                a2 = np.radians(entity.dxf.end_angle)
                t = np.linspace(a1, a2, 50)
                x_arc = cx + r * np.cos(t)
                y_arc = cy + r * np.sin(t)
                ax.plot(x_arc, y_arc, color=_aci_color(color_val),
                       linewidth=_lineweight_to_px(getattr(entity.dxf, 'lineweight', 35)))
                
            elif entity.dxftype() == 'LWPOLYLINE':
                pts = np.array(list(entity.get_points()))
                if len(pts) > 1:
                    closed = entity.closed
                    ax.plot(pts[:,0], pts[:,1], color=_aci_color(color_val),
                           linewidth=_lineweight_to_px(getattr(entity.dxf, 'lineweight', 35)),
                           linestyle='-')
                    if closed:
                        ax.plot([pts[-1,0], pts[0,0]], [pts[-1,1], pts[0,1]],
                               color=_aci_color(color_val))

            elif entity.dxftype() == 'TEXT':
                ins = entity.dxf.insert
                text = entity.dxf.text or ''
                h = entity.dxf.height
                ax.text(ins[0], ins[1], text, fontsize=h*3,
                       color=_aci_color(color_val))

        except Exception:
            continue
    
    fig.savefig(output_path, format='svg', facecolor='white',
               bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)


# ━━━━━━━━━ 颜色映射 ━━━━━━━━━

_ACI_COLORS = {
    1: '#FF0000', 2: '#FFFF00', 3: '#00FF00', 4: '#00FFFF',
    5: '#0000FF', 6: '#FF00FF', 7: '#FFFFFF', 8: '#808080',
    9: '#C0C0C0', 250: '#000000', 251: '#111111', 252: '#222222',
    253: '#333333', 254: '#444444', 255: '#555555', 256: '#666666',
}

def _aci_color(index: int) -> str:
    return _ACI_COLORS.get(index, '#000000')

def _lineweight_to_px(lw: int) -> float:
    """将 DXF 线重 (1/100mm) 转换为 matplotlib 线宽"""
    if lw <= 0:
        return 0.5
    return min(max(lw / 35 * 0.5, 0.3), 5.0)
