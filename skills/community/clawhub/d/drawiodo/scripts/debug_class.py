import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")
from drawio_unified import topological_layer, generate_diagram
from collections import defaultdict
from drawio_route import Rect

# === Class Diagram ===
nodes = [
    {'id': 'User', 'label': 'User'},
    {'id': 'Order', 'label': 'Order'},
    {'id': 'Product', 'label': 'Product'},
    {'id': 'Payment', 'label': 'Payment'},
    {'id': 'CartItem', 'label': 'CartItem'},
    {'id': 'OrderItem', 'label': 'OrderItem'},
]
edges = [
    {'from': 'User', 'to': 'Order', 'label': '1 → *'},
    {'from': 'User', 'to': 'CartItem', 'label': '1 → *'},
    {'from': 'Order', 'to': 'OrderItem', 'label': '1 → *'},
    {'from': 'Product', 'to': 'OrderItem', 'label': '1 → *'},
    {'from': 'Product', 'to': 'CartItem', 'label': '1 → *'},
    {'from': 'Order', 'to': 'Payment', 'label': '1 → 1'},
]

layers = topological_layer(nodes, edges)
print('=== Layers ===')
for lvl in sorted(set(layers.values())):
    names = [n['id'] for n in nodes if layers[n['id']] == lvl]
    print(f'  Layer {lvl}: {names}')

builder = generate_diagram(nodes, edges, 'Class Test')

print()
print('=== Node Positions ===')
for n in builder.nodes:
    print(f'  {n.label}: x={n.x:.0f} y={n.y:.0f} w={n.width:.0f} h={n.height:.0f}')

print()
print('=== Edge Analysis ===')
for e in builder.edges:
    src = next(n for n in builder.nodes if n.id == e.source_id)
    tgt = next(n for n in builder.nodes if n.id == e.target_id)

    # Full path
    pts = [(src.x+src.width/2, src.y+src.height/2)]
    pts.extend(e.waypoints or [])
    pts.append((tgt.x+tgt.width/2, tgt.y+tgt.height/2))

    # Path midpoint
    total_len = sum(abs(pts[i+1][0]-pts[i][0])+abs(pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1))
    half = total_len / 2
    acc = 0
    lx, ly = pts[0]
    for i in range(len(pts)-1):
        seg = abs(pts[i+1][0]-pts[i][0]) + abs(pts[i+1][1]-pts[i][1])
        if acc + seg >= half:
            frac = (half - acc) / max(seg, 1)
            lx = pts[i][0] + (pts[i+1][0]-pts[i][0]) * frac
            ly = pts[i][1] + (pts[i+1][1]-pts[i][1]) * frac
            break
        acc += seg

    collisions = []
    for n2 in builder.nodes:
        if n2.id in (e.source_id, e.target_id):
            continue
        if n2.x <= lx <= n2.x+n2.width and n2.y <= ly <= n2.y+n2.height:
            collisions.append(n2.label)

    s_l = next(n.label for n in builder.nodes if n.id == e.source_id)
    t_l = next(n.label for n in builder.nodes if n.id == e.target_id)
    wp_str = ' '.join(f'({wp[0]:.0f},{wp[1]:.0f})' for wp in (e.waypoints or []))

    if collisions:
        print(f'  ❌ {s_l}→{t_l} "{e.label}" label=({lx:.0f},{ly:.0f}) IN {collisions}')
        print(f'      wp: {wp_str}')
    else:
        print(f'  ✅ {s_l}→{t_l} "{e.label}" label=({lx:.0f},{ly:.0f})')
        print(f'      wp: {wp_str}')
