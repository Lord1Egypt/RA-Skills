<!-- Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran". MIT License: see LICENSE.md. -->
# Forklift Fault Diagnosis

Organize diagnosis as symptom → possible cause → confirming check → remedy. This is the mechanism reference for electric and IC counterbalanced trucks. For a specific truck and fault, use `after-sales-service.md` and search `after-sales-cases.md`; actual measurements prevail over anecdotes.

## 1. Preparation

Qualified personnel may require a suitable multimeter, current clamp, pressure gauge, temperature instrument, manufacturer diagnostic tool, insulation tester and inspection tools. Instrument ratings and test methods must match the truck. Insulation testing requires isolation of sensitive electronics according to the manual.

Secure and unload the truck, lower forks, apply lockout/tagout and use wheel chocks as required. Raised components require approved supports. Release stored hydraulic energy before opening a circuit. Never enter an unsupported mast or work on a live traction battery. Post-repair tests require a safe area and competent operator.

All voltage, pressure, temperature, clearance and resistance limits are model-specific. Generic figures are not adjustment targets.

## 2. Electric Trucks

### 2.1 No power / no start / no travel

Check in order: emergency stop and reason for activation; operator presence/restraint; neutral startup condition; SOC and accessible power connections; main fuse/contactor; auxiliary DC-DC supply; exact controller code; accelerator movement and signal. Operate interlocks correctly; never bypass them. Electrical measurements and component replacement require appropriately qualified personnel and the correct manual.

### 2.2 Weak or slow travel

Check battery SOC, cell condition, thermal derating, cooling, controller codes, tyre pressure, dragging brakes/bearings, accelerator signal and encoder feedback. Hydraulic-drive trucks also require pump/motor assessment. Do not defeat protective current or temperature limits. Compare cell imbalance with the actual chemistry and manufacturer limits.

### 2.3 Weak or slow lift

Verify load against the actual residual-capacity plate first; any overload is unacceptable. Then check oil level/condition/temperature, filter restriction, visible leaks, pump noise and codes. A technician can distinguish relief-valve, pump, spool and cylinder leakage using specified tests. Set pressure only to the manufacturer's specification, never to lift an overload.

### 2.4 Charging problems

Check approved charger compatibility, supply, connector condition, charger code, battery temperature permission, BMS communication and cell condition. Do not force charging through a BMS lockout or substitute an incompatible lead-acid/lithium charger. Stop for arcing, smoke, swelling or abnormal heat; escalate electrical and internal battery work.

### 2.5 Battery degradation

| Symptom | Possible causes | Confirmation |
|---|---|---|
| Shorter runtime | Ageing, weak cells, changed duty or temperature | Comparable-duty records and approved capacity test |
| SOC jumps | Estimation or imbalance | BMS history and manufacturer calibration procedure |
| Charging heat | Resistance, connector or cooling fault | Stop and obtain specialist inspection |
| Persistently low cell | Cell or connection fault | Battery specialist assessment |
| Rapid standing loss | Self-discharge, leakage, auxiliary load | Qualified electrical diagnosis |

SOH = measured usable capacity / rated capacity under stated test conditions. Rate, temperature and cutoff must match the approved procedure. A generic 1C full discharge or one universal retirement percentage is unsuitable for every battery.

## 3. Internal-Combustion Trucks

### 3.1 Engine will not start

Check fuel, starting battery/connections, starter/relay, permitted startup conditions, filter/air ingress, codes and ignition components where applicable. Use the actual nominal supply voltage: do not apply a 22 V threshold to a 12 V starting system. High-pressure fuel/injector work requires qualified personnel.

### 3.2 Low engine power

Investigate intake and fuel filters, fuel air ingress, injectors, boost leaks, turbocharger, DPF, EGR, intercooler and cooling. Regeneration must follow the manual with fire and ventilation controls; never defeat emissions equipment.

### 3.3 Exhaust colour

| Colour | Possible causes | Investigation |
|---|---|---|
| Black | Restricted air or excess fuel | Intake, filters, injection |
| Blue | Oil consumption, rings or seals | Oil history, compression, turbo |
| White | Cold combustion, atomization or coolant ingress | Temperature, injectors, coolant, gasket |
| Grey | Oil or combustion fault | Engine-specific assessment |

Colour is a clue, not a confirmed diagnosis. Do not operate IC trucks in inadequately ventilated spaces.

### 3.4 Transmission noise / harsh shifting

Speed-related noise can involve gears; load-related noise can involve bearings. Harsh engagement can involve clutch, torque converter, oil or controls. Check fluid specification/level and codes before specialist teardown.

## 4. Hydraulics

| Symptom | Possible causes | Check path |
|---|---|---|
| Weak lift | Load, oil, restriction, relief valve, pump | Capacity → fluid → filter → specified pressure test |
| Fork drift | Cylinder or valve leakage | Approved drift/leakage test with exclusion zone |
| Heavy steering | Supply, priority valve, steering unit | Mechanical inspection then correct circuit test |
| Pulling | Tyres, linkage, cylinder or valve | Mechanical checks before hydraulic diagnosis |
| Valve leak | Seals, connections, spool | Isolate and repair to manual |
| Excess heat | Cooling restriction, bypassing valve, duty | Cooling → load/duty → circuit testing |

Main relief, lift, tilt, steering and priority-valve ports/pressures differ by truck. Never loosen a fitting to test pressure or search for a pinhole leak with a hand.

## 5. Auxiliary Electrical Systems

All lights/horn/instruments failing suggests supply, main fuse or ground. A single failure suggests its fuse, wire, switch, device or ground. Erratic readings can involve sensor supply, signal, ground or communications. Sensor resistance, Hall voltage and angle output are not universal; use the correct wiring diagram.

## 6. Mast and Forks

Jerky lift can involve chains, rollers, air or hydraulics. Drift can involve cylinder/valve leakage. Noise can involve lubrication, rollers and bearings. Uneven carriage can involve chains or structure. Cracked forks/mast require immediate withdrawal and approved replacement/assessment, not improvised welding.

## 7. Brakes

Long stopping distance: wear, air, contamination or assist failure. Pulling: unequal contamination or seized cylinder. Drag: clearance, return mechanism or controls. Parking failure: cable, actuator or mechanism. Regeneration failure: feedback/control fault. Repair and verify through a competent technician; regeneration does not replace required service braking.

## 8. Tyres

Check pneumatic pressure against the truck/tyre specification; underpressure causes heat and wear, overpressure affects grip and ride. Inspect solid tyres against wear marks and damage limits. Rotation or conversion requires approval because stability and loading may change. A metal ring is not generic explosion protection.

## 9. Diagnostic Overview

```text
No movement → supply / startup conditions / emergency stop / neutral / presence
Slow travel → battery / thermal limits / drag / feedback
Weak lift → load / oil / filter / pressure / pump / valve / cylinder
Charging → compatibility / supply / connector / temperature / BMS
Engine → starting supply / fuel / air / ignition or injection / codes
Other → electrical / mast / brake / tyre assessment
```

## 10. Escalation

Stop and escalate burnt/wet controllers, thermal battery warnings, internal battery/high-voltage faults, hydraulic teardown, low engine compression, transmission teardown, structural cracks and any explosion-protected truck repair. Never continue using unsafe equipment.

## 11. Records and Spares

Record symptoms, dates, measurements, codes, diagnosis confidence, actual repairs, part/batch numbers, technician, downtime, fluid/battery history, statutory inspections and next maintenance. Separate proposed from completed work.

Typical stock includes approved filters, friction parts, seals, contactors, sensors and rollers. Heli K2/H3, Hangcha XE/A, BYD, Linde H30/H35, Toyota 8FBE and LiuGong CPCD30 require serial-specific catalogues. Do not assume controllers, batteries, chargers or brushes interchange. See `parts-consumables.md` and `maintenance-plan.md`.
