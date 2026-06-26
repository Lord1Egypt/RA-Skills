"""DXF → PDF 导出"""


def dxf_to_pdf(doc, output_path: str,
               width: int = 800,
               height: int = 600,
               dpi: int = 150):
    """
    导出为 PDF 文件
    先通过 matplotlib 渲染再保存 PDF
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from .to_svg import _dxf_to_svg_fallback, _aci_color, _lineweight_to_px

    # 复用 SVG 渲染逻辑但输出 PDF
    all_pts = []
    for entity in doc.modelspace():
        try:
            if entity.dxftype() == 'LINE':
                all_pts.extend([(entity.dxf.start.x, entity.dxf.start.y),
                                (entity.dxf.end.x, entity.dxf.end.y)])
            elif entity.dxftype() in ('CIRCLE', 'ARC'):
                c = (entity.dxf.center.x, entity.dxf.center.y)
                all_pts.append(c)
                r = entity.dxf.radius
                all_pts.append((c[0]+r, c[1]+r))
            elif entity.dxftype() == 'LWPOLYLINE':
                all_pts.extend(list(entity.get_points()))
        except Exception:
            continue

    if not all_pts:
        fig = plt.figure()
        plt.savefig(output_path, format='pdf')
        plt.close()
        return

    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    
    mx, Mx = min(xs), max(xs)
    my, My = min(ys), max(ys)
    pad = max(Mx-mx, My-my) * 0.08

    fig, ax = plt.subplots(1, 1, figsize=(width/100, height/100), dpi=dpi)
    ax.set_xlim(mx-pad, Mx+pad)
    ax.set_ylim(my-pad, My+pad)
    ax.set_aspect('equal')
    ax.axis('off')

    for entity in doc.modelspace():
        try:
            cv = _aci_color(getattr(entity.dxf, 'color', 7))
            lw = _lineweight_to_px(getattr(entity.dxf, 'lineweight', 35))

            if entity.dxftype() == 'LINE':
                ax.plot([entity.dxf.start.x, entity.dxf.end.x],
                       [entity.dxf.start.y, entity.dxf.end.y],
                       color=cv, linewidth=lw)

            elif entity.dxftype() == 'CIRCLE':
                circle = plt.Circle(
                    (entity.dxf.center.x, entity.dxf.center.y),
                    entity.dxf.radius, fill=False,
                    edgecolor=cv, linewidth=lw)
                ax.add_patch(circle)

            elif entity.dxftype() == 'ARC':
                cx, cy = entity.dxf.center.x, entity.dxf.center.y
                r = entity.dxf.radius
                a1, a2 = np.radians(entity.dxf.start_angle), np.radians(entity.dxf.end_angle)
                t = np.linspace(a1, a2, 50)
                ax.plot(cx + r*np.cos(t), cy + r*np.sin(t), color=cv, linewidth=lw)

            elif entity.dxftype() == 'LWPOLYLINE':
                pts = np.array(list(entity.get_points()))
                if len(pts) > 1:
                    ax.plot(pts[:,0], pts[:,1], color=cv, linewidth=lw)
                    if entity.closed:
                        ax.plot([pts[-1,0],pts[0,0]], [pts[-1,1],pts[0,1]], color=cv)

            elif entity.dxftype() == 'TEXT':
                ax.text(entity.dxf.insert.x, entity.dxf.insert.y,
                       entity.dxf.text or '', fontsize=entity.dxf.height*3, color=cv)

        except Exception:
            continue

    fig.savefig(output_path, format='pdf', facecolor='white',
               bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
