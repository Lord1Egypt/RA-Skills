from pathlib import Path

p = Path('src/cortex/self-evolution/self-evolution-core.js')
lines = p.read_text(encoding='utf-8').splitlines()

# 1. Fix previousImprovement initialization (line 267, 0-indexed 266)
if 'Infinity' in lines[266]:
    lines[266] = '    let previousImprovement = null;'
    print('FIXED: Infinity -> null')
else:
    print('SKIP: line 267 already', repr(lines[266]))

# 2. Add baselineWeaknessCount after iterationHistory
insert_idx = None
for i, line in enumerate(lines):
    if 'const iterationHistory = []' in line:
        insert_idx = i + 1
        break
if insert_idx is not None:
    lines.insert(insert_idx, '    const baselineWeaknessCount = (learning.weaknesses || []).length;')
    print(f'INSERTED baselineWeaknessCount at line {insert_idx+1}')
else:
    print('ERROR: iterationHistory line not found')

# 3. Fix convergence check
text = '\n'.join(lines)

old_block = """      if (iterationCount > 1) {

        const improvementDelta = Math.abs(previousImprovement - currentImprovement);

        if (improvementDelta < convergenceThreshold) {

          converged = true;

        }

      }

      previousImprovement = currentImprovement;"""

new_block = """      if (iterationCount > 1 && previousImprovement !== null) {
        const improvementDelta = Math.abs(previousImprovement - currentImprovement);
        if (improvementDelta < convergenceThreshold) {
          converged = true;
        }
      }

      previousImprovement = currentImprovement;"""

if old_block in text:
    text = text.replace(old_block, new_block, 1)
    print('FIXED: convergence check')
else:
    print('ERROR: convergence block not found')
    idx = text.find('iterationCount > 1')
    print(repr(text[idx-20:idx+250]))

p.write_text(text, encoding='utf-8')
print('WRITTEN OK')
