# System Engineering Conventions

# System elements

Use stable IDs:

SYS-CMP-### : system component
SYS-IF-###  : interface
SYS-MODE-### : operational mode
SYS-FUNC-### : function

# Interfaces

Every significant interface must define when applicable:

- ID;
- source;
- destination;
- direction;
- data/signals;
- units;
- range;
- precision;
- timing;
- latency;
- update rate;
- protocol;
- error behavior;
- initialization;
- timeout;
- degraded behavior;
- cybersecurity constraints.

# Interface Control

For complex interfaces, create an ICD or equivalent.

A baselined interface must not change silently.

# System Architecture

Each component must have:
- responsibility;
- allocated requirements;
- interfaces;
- dependencies;
- modes/states;
- resource constraints when relevant.

# Units

Preferably use SI units.

Any exception must be clear.

Never leave a physical value without a unit when the unit is necessary for its interpretation.

# States and Modes

For systems with multiple states:
- explicitly name the modes;
- define transitions;
- triggers;
- guards;
- actions;
- illegal transitions;
- degraded modes;
- startup/shutdown behavior.

# Error and degraded behavior

Fault behaviors must be specified on the same basis as nominal behavior when relevant.
