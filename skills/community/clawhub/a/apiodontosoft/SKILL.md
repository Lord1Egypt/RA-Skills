---
name: odontosoft
description: Gestiona turnos odontológicos en Odontosoft. Usar cuando el usuario quiera consultar doctores disponibles, ver turnos libres de un odontólogo, buscar un paciente por documento, o agendar un nuevo turno dental. Configurar ODONTOSOFT_BASE_URL y ODONTOSOFT_TOKEN antes de usar.
---

# Odontosoft

Conecta con la API REST de Odontosoft usando las herramientas definidas en `manifest.json`.

## Herramientas disponibles

- **get_doctores** — Lista los odontólogos activos de la clínica
- **get_turnos_disponibles** — Horarios libres de un doctor en una fecha (`doctor_id`, `fecha`)
- **buscar_paciente** — Busca paciente por número de documento (`documento`)
- **agendar_turno** — Crea un turno (`paciente_id`, `doctor_id`, `fecha`, `hora`, `motivo`)

## Flujo recomendado para agendar

1. `get_doctores` → elegir doctor
2. `get_turnos_disponibles` → confirmar slot libre
3. `buscar_paciente` → obtener `paciente_id`
4. Confirmar datos con el usuario
5. `agendar_turno`
