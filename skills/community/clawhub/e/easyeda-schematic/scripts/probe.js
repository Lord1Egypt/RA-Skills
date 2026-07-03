// One-shot full-layout pull: components + pins + flags + wires.
// Everything the linter needs to find problems WITHOUT screenshots.
const out = { parts: [], flags: [], wires: [] };

const comps = await eda.sch_PrimitiveComponent.getAll();
for (const c of comps) {
  const type = c.getState_ComponentType();
  const rec = {
    pid: c.getState_PrimitiveId(),
    type,
    designator: c.getState_Designator(),
    net: c.getState_Net(),
    x: c.getState_X(), y: c.getState_Y(),
    rotation: c.getState_Rotation(),
    mirror: c.getState_Mirror(),
  };
  if (type === 'part') {
    try {
      const pins = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(rec.pid);
      rec.pins = (pins ?? []).map(p => ({
        num: p.getState_PinNumber(), name: p.getState_PinName(),
        x: p.getState_X(), y: p.getState_Y(),
      }));
      if (rec.pins.length) {
        const xs = rec.pins.map(p => p.x), ys = rec.pins.map(p => p.y);
        rec.bbox = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
      }
    } catch (e) { rec.pinErr = e.message; }
    out.parts.push(rec);
  } else if (type === 'netflag' || type === 'netport') {
    out.flags.push(rec);
  } else {
    out.parts.push(rec); // sheet etc
  }
}

try {
  const ws = await eda.sch_PrimitiveWire.getAll();
  for (const w of ws) {
    out.wires.push({
      pid: w.getState_PrimitiveId(),
      net: w.getState_Net(),
      line: w.getState_Line ? w.getState_Line() : null,
    });
  }
} catch (e) { out.wireErr = e.message; }

return out;
