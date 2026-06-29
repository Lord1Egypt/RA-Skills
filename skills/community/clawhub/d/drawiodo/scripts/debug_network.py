import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")
from drawio_unified import generate_diagram
from drawio_route import Rect

# === Network Topology ===
nodes = [
    {'id': 'Core-SW1', 'label': 'Core-SW1'},
    {'id': 'Core-SW2', 'label': 'Core-SW2'},
    {'id': 'Dist-SW1', 'label': 'Dist-SW1'},
    {'id': 'Dist-SW2', 'label': 'Dist-SW2'},
    {'id': 'Dist-SW3', 'label': 'Dist-SW3'},
    {'id': 'Access-SW1', 'label': 'Access-SW1'},
    {'id': 'Access-SW2', 'label': 'Access-SW2'},
    {'id': 'Firewall-1', 'label': 'Firewall-1'},
    {'id': 'LoadBalancer', 'label': 'LoadBalancer'},
    {'id': 'Web-S1', 'label': 'Web-Server-1'},
    {'id': 'Web-S2', 'label': 'Web-Server-2'},
    {'id': 'App-S1', 'label': 'App-Server-1'},
    {'id': 'App-S2', 'label': 'App-Server-2'},
    {'id': 'DB-M', 'label': 'DB-Master'},
    {'id': 'DB-S', 'label': 'DB-Slave'},
]
edges = [
    {'from': 'Core-SW1', 'to': 'Dist-SW1', 'label': '40Gbps'},
    {'from': 'Core-SW1', 'to': 'Dist-SW2', 'label': '40Gbps'},
    {'from': 'Core-SW2', 'to': 'Dist-SW2', 'label': '40Gbps'},
    {'from': 'Core-SW2', 'to': 'Dist-SW3', 'label': '40Gbps'},
    {'from': 'Dist-SW1', 'to': 'Access-SW1', 'label': '10Gbps'},
    {'from': 'Dist-SW1', 'to': 'Access-SW2', 'label': '10Gbps'},
    {'from': 'Dist-SW2', 'to': 'Access-SW1', 'label': '10Gbps'},
    {'from': 'Dist-SW2', 'to': 'Firewall-1', 'label': '10Gbps'},
    {'from': 'Dist-SW3', 'to': 'Access-SW2', 'label': '10Gbps'},
    {'from': 'Dist-SW3', 'to': 'LoadBalancer', 'label': '10Gbps'},
    {'from': 'Access-SW1', 'to': 'Web-S1', 'label': '1Gbps'},
    {'from': 'Access-SW1', 'to': 'Web-S2', 'label': '1Gbps'},
    {'from': 'Access-SW2', 'to': 'Web-S1', 'label': '1Gbps'},
    {'from': 'Access-SW2', 'to': 'Web-S2', 'label': '1Gbps'},
    {'from': 'Firewall-1', 'to': 'App-S1', 'label': '1Gbps'},
    {'from': 'Firewall-1', 'to': 'App-S2', 'label': '1Gbps'},
    {'from': 'LoadBalancer', 'to': 'App-S1', 'label': '1Gbps'},
    {'from': 'LoadBalancer', 'to': 'App-S2', 'label': '1Gbps'},
    {'from': 'Web-S1', 'to': 'App-S1', 'label': 'API'},
    {'from': 'Web-S2', 'to': 'App-S2', 'label': 'API'},
    {'from': 'App-S1', 'to': 'DB-M', 'label': 'JDBC'},
    {'from': 'App-S2', 'to': 'DB-S', 'label': 'JDBC'},
    {'from': 'DB-M', 'to': 'DB-S', 'label': 'Replication'},
]
builder = generate_diagram(nodes, edges, 'Network Test')

print('=== Node Positions ===')
for n in builder.nodes:
    print(f'  {n.label}: x={n.x:.0f} y={n.y:.0f} w={n.width:.0f} h={n.height:.0f}')

print()
print('=== Edge Lanes + Labels ===')
for e in builder.edges:
    src = next(n for n in builder.nodes if n.id == e.source_id)
    tgt = next(n for n in builder.nodes if n.id == e.target_id)
    s_l = next(n.label for n in builder.nodes if n.id == e.source_id)
    t_l = next(n.label for n in builder.nodes if n.id == e.target_id)
    wp_str = ' '.join(f'({wp[0]:.0f},{wp[1]:.0f})' for wp in (e.waypoints or []))

    # Label midpoint
    pts = [(src.x+src.width/2, src.y+src.height/2)]
    pts.extend(e.waypoints or [])
    pts.append((tgt.x+tgt.width/2, tgt.y+tgt.height/2))
    total = sum(abs(pts[i+1][0]-pts[i][0])+abs(pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1))
    half = total / 2; acc = 0; lx, ly = pts[0]
    for i in range(len(pts)-1):
        seg = abs(pts[i+1][0]-pts[i][0])+abs(pts[i+1][1]-pts[i][1])
        if acc+seg >= half:
            frac = (half-acc)/max(seg,1); lx = pts[i][0]+(pts[i+1][0]-pts[i][0])*frac; ly = pts[i][1]+(pts[i+1][1]-pts[i][1])*frac
            break
        acc+=seg

    # Check collisions
    collisions = []
    for n2 in builder.nodes:
        if n2.id in (e.source_id, e.target_id): continue
        if n2.x <= lx <= n2.x+n2.width and n2.y <= ly <= n2.y+n2.height:
            collisions.append(n2.label)

    # Check wp for uniqueness
    wp_x_positions = [wp[0] for wp in (e.waypoints or [])]
    unique_x = len(set(wp_x_positions)) if wp_x_positions else 0

    mk = '❌' if collisions else ('⚠️' if unique_x <= 1 and len(wp_x_positions) >= 2 else '✅')
    label_str = f'"{e.label}"' if e.label else '(no label)'
    coll_str = f' IN {collisions}' if collisions else ''
    print(f'  {mk} {s_l}→{t_l} {label_str} lane_x={wp_x_positions[0] if wp_x_positions else "?":.0f} label=({lx:.0f},{ly:.0f}){coll_str}')
    print(f'      wp: {wp_str}')
