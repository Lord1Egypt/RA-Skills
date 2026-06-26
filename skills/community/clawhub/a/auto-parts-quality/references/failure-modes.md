# Failure Mode Library - Fuel System Components

## HPFP (High Pressure Fuel Pump)

### 1. Seizure/Jamming

**Symptoms:**
- Pump cannot rotate
- Engine stall
- Unusual noise during operation

**Root Causes:**

| Category | Specific Cause | Evidence |
|----------|---------------|----------|
| **Surface** | Honing pattern insufficient (RVK too shallow, angle wrong) | Microscope: shallow valleys, smooth surface |
| **Surface** | DLC coating damage | Microscope: coating chip-off, exposed substrate |
| **Surface** | Scoring from contamination | SEM: embedded particles, linear scratches |
| **Dimensional** | Clearance too tight (thermal expansion) | Measurement: dimensions at low end of tolerance |
| **Material** | Surface hardness insufficient | Hardness test: below specification |
| **Lubrication** | Oil starvation | Oil passage blockage, low oil pressure |

**Investigation Steps:**
1. Measure RVK, RPK, RZ against OE parts
2. Compare honing angle with specification
3. Check oil passages for blockage
4. Review hardness test results
5. Analyze particle composition from cleanliness test

---

### 2. Internal Leakage

**Symptoms:**
- Pressure drop below specification
- Fuel consumption increase
- Engine performance degradation

**Root Causes:**

| Category | Specific Cause | Evidence |
|----------|---------------|----------|
| **Valve** | Valve seat wear | Microscope: wear pattern on seat |
| **Valve** | Valve spring fatigue | Spring force measurement below spec |
| **Valve** | Foreign material on seat | Microscope: embedded particle |
| **Sealing** | Seal surface damage | Microscope: scratches, deformations |
| **Sealing** | Seal aging/hardening | Visual: cracks, permanent set |

**Investigation Steps:**
1. Disassemble and inspect valve train
2. Measure spring free length and force
3. Check seal surfaces under microscope
4. Review cleaning/particle analysis results

---

### 3. External Leakage

**Symptoms:**
- Fuel odor
- Visible fuel seepage
- Pressure drop over time

**Root Causes:**

| Category | Specific Cause | Evidence |
|----------|---------------|----------|
| **Connector** | Thread damage | Visual: crossed threads, missing thread starts |
| **Connector** | Fitting not torqued properly | Torque verification, witness mark check |
| **Connector** | Debris in thread | Visual: contamination in threads |
| **Seal** | O-ring damage | Visual: cut, deformation, aging |
| **Housing** | Crack (stress or thermal) | Visual: crack, fluorescent dye test |

**Investigation Steps:**
1. Inspect connector threads
2. Check torque specifications
3. Verify O-ring condition
4. Pressure test to locate leak point

---

### 4. Noise/Vibration

**Symptoms:**
- Abnormal noise during operation
- Vibration felt through structure

**Root Causes:**

| Category | Specific Cause | Evidence |
|----------|---------------|----------|
| **Mechanical** | Bearing failure | Noise frequency analysis, visual |
| **Mechanical** | Rattle from loose part | Visual inspection, shake test |
| **Hydraulic** | Cavitation | Noise characteristics, air in system |
| **Mechanical** | Buffer pad broken | Disassembly: fragmented buffer |

**Investigation Steps:**
1. Noise frequency analysis
2. Disassemble and inspect components
3. Check buffer pad condition
4. Verify mounting torque

---

## Fuel Injector

### 1. Nozzle Clogging

**Symptoms:**
- Fuel spray pattern abnormal
- Engine misfire
- Power loss

**Root Causes:**
- Fuel contamination (particles, water)
- Internal corrosion from low-quality fuel
- coking from high temperature operation

---

### 2. Leakage at Fitting

**Symptoms:**
- External fuel leak
- Pressure drop

**Root Causes:**
- Misfit during assembly
- Damaged sealing surfaces
- Incorrect torque sequence

---

## General Guidelines

### Microscope Inspection Checklist

For honing pattern evaluation:
- [ ] Overall pattern visibility (should show clear cross-hatch)
- [ ] Valley depth (RVK should be measurable)
- [ ] Peak height (RPK within spec)
- [ ] Angle consistency (should match specification)
- [ ] Surface randomness (no unidirectional patterns)
- [ ] Embedded particles (indicates contamination source)

### Cleanliness Analysis Interpretation

| Particle Size | Likely Source | Implication |
|---------------|--------------|-------------|
| > 50 μm | Assembly/handling | Major contamination |
| 10-50 μm | Internal wear | Normal or abnormal depending on rate |
| < 10 μm | System-generated | May indicate running-in wear |

**Key indicator:** Particles matching housing/plate material composition suggest internal origin; particles with external composition (dust, debris) suggest contamination.

### Comparison with OE Parts

Always compare suspect parts with OE reference parts using:
1. Microscope at same magnification
2. Roughness profilometer with same measurement settings
3. Visual inspection under same lighting angle

Document differences with photos for reporting.
