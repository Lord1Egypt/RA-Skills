"""Debug: trace what happens with Z-path for L0-L1 edges"""
import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")

# Monkey-patch _compute_with_lane to trace
import drawio_unified as du

original = du._compute_with_lane

def traced_compute(src, tgt, src_port, tgt_port, router, lane_x, crossing=False, h_y=None, label="", positions=None, exclude=None):
    if h_y is not None and not crossing:
        sx = src.x + src.width/2
        sy = src.y + src.height
        tx = tgt.x + tgt.width/2
        ty = tgt.y
        y_min = sy + 12
        y_max = ty - 12
        src_label = src.label if hasattr(src, 'label') else src.id
        tgt_label = tgt.label if hasattr(tgt, 'label') else tgt.id
        hy_disp = f"{h_y:.1f}" if h_y else "NONE"
        print(f"  Z-path check: {src_label}->{tgt_label} lane={lane_x:.1f} h_y={hy_disp} y_range=[{y_min:.0f},{y_max:.0f}]")
    return original(src, tgt, src_port, tgt_port, router, lane_x, crossing, h_y, label, positions, exclude)

du._compute_with_lane = traced_compute

# Build mini test: Core -> Dist
nodes = [
    {'id': 'CS1', 'label': 'Core-SW1'},
    {'id': 'CS2', 'label': 'Core-SW2'},
    {'id': 'DS1', 'label': 'Dist-SW1'},
    {'id': 'DS2', 'label': 'Dist-SW2'},
    {'id': 'DS3', 'label': 'Dist-SW3'},
]
edges = [
    {'from': 'CS1', 'to': 'DS1', 'label': '40Gbps'},
    {'from': 'CS1', 'to': 'DS2', 'label': '40Gbps'},
    {'from': 'CS2', 'to': 'DS2', 'label': '40Gbps'},
    {'from': 'CS2', 'to': 'DS3', 'label': '40Gbps'},
]

print("=" * 60)
builder = du.generate_diagram(nodes, edges, "Test Core-Dist")
print("=" * 60)

# Show final output
for e in builder.edges:
    src = next(n.label for n in builder.nodes if n.id == e.source_id)
    tgt = next(n.label for n in builder.nodes if n.id == e.target_id)
    wps = ' '.join(f'({wp[0]:.0f},{wp[1]:.0f})' for wp in (e.waypoints or []))
    print(f"  RESULT: {src}->{tgt} [{wps}]")
