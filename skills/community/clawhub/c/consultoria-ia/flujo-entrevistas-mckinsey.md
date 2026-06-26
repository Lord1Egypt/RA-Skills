# 🔄 FLUJO: Entrenamiento de Entrevistas (Metodología McKinsey)

## 🎯 Objetivo
Entrenarte para conducir entrevistas de diagnóstico que identifiquen problemas reales y oportunidades de IA en PYMES, usando la metodología estructurada de McKinsey.

## 📋 Fases del Flujo

### FASE 1: PREPARACIÓN (Pre-interview)
```
┌─────────────────────────────────────────────┐
│ 1. Análisis preliminar del negocio          │
│ 2. Definición de hipótesis iniciales        │
│ 3. Preparación de guía de preguntas         │
│ 4. Identificación de stakeholders clave     │
└─────────────────────────────────────────────┘
```

**Herramientas:**
- Template: `consultoria/templates/analisis-preliminar.md`
- Checklist: `consultoria/checklists/preparacion-entrevista.md`
- Guía de preguntas por vertical (retail, salud, logística)

### FASE 2: EJECUCIÓN (Interview)
```
┌─────────────────────────────────────────────┐
│ 1. Apertura: Contexto y objetivos           │
│ 2. Exploración: Pain points actuales        │
│ 3. Diagnóstico: Causa raíz (5 Whys)         │
│ 4. Cuantificación: Impacto económico        │
│ 5. Cierre: Siguientes pasos                 │
└─────────────────────────────────────────────┘
```

**Técnicas McKinsey:**
- **MECE:** Mutuamente Excluyente, Colectivamente Exhaustivo
- **Issue Tree:** Descomposición estructurada del problema
- **Hypothesis-driven:** Validar/invalidar hipótesis con datos
- **So what?:** Conectar hallazgos con implicaciones de negocio

### FASE 3: SÍNTESIS (Post-interview)
```
┌─────────────────────────────────────────────┐
│ 1. Consolidación de hallazgos               │
│ 2. Priorización de oportunidades            │
│ 3. Estimación preliminar de ROI             │
│ 4. Propuesta de next steps                  │
└─────────────────────────────────────────────┘
```

**Entregables:**
- Memo de diagnóstico (1-2 páginas)
- Matriz de oportunidades priorizadas
- Estimación de impacto económico
- Recomendaciones de implementación

## 🛠️ Templates y Herramientas

### 1. Guía de Preguntas por Vertical
```markdown
# Retail/E-commerce
- ¿Cuál es tu tasa de conversión actual?
- ¿Cómo manejas el inventario y predicción de demanda?
- ¿Qué porcentaje de consultas de clientes son repetitivas?
- ¿Cómo optimizas precios según competencia y temporada?

# Salud/Clínicas  
- ¿Cuál es tu tasa de ausentismo en turnos?
- ¿Cómo manejas historias clínicas y seguimiento?
- ¿Qué procesos administrativos consumen más tiempo?
- ¿Cómo gestionas recordatorios y confirmaciones?

# Agro-tech/Logística
- ¿Cómo planificas rutas de distribución?
- ¿Qué porcentaje de pérdida tienes post-cosecha?
- ¿Cómo realizas control de calidad?
- ¿Qué datos capturas pero no analizas?
```

### 2. Checklist de Preparación
```markdown
- [ ] Investigar sitio web/redes del cliente
- [ ] Revisar industria y competidores
- [ ] Preparar 3 hipótesis iniciales
- [ ] Definir métricas clave a explorar
- [ ] Preparar demo relevante (si aplica)
- [ ] Confirmar stakeholders presentes
```

### 3. Template de Memo de Diagnóstico
```markdown
# DIAGNÓSTICO: [Nombre Cliente] - [Fecha]

## 1. Contexto del Negocio
[Descripción breve, industria, tamaño, desafíos conocidos]

## 2. Hallazgos Principales
### 2.1 Pain Points Identificados
1. [Problema 1] - Impacto estimado: [% o $]
2. [Problema 2] - Impacto estimado: [% o $]
3. [Problema 3] - Impacto estimado: [% o $]

### 2.2 Oportunidades de IA
1. [Oportunidad 1] - ROI potencial: [% o $]
2. [Oportunidad 2] - ROI potencial: [% o $]
3. [Oportunidad 3] - ROI potencial: [% o $]

## 3. Recomendaciones Prioritarias
### Prioridad Alta (0-3 meses)
1. [Recomendación 1] - Esfuerzo: [bajo/medio/alto]
2. [Recomendación 2] - Esfuerzo: [bajo/medio/alto]

### Prioridad Media (3-6 meses)
1. [Recomendación 3] - Esfuerzo: [bajo/medio/alto]

## 4. Siguientes Pasos
- [ ] [Acción 1] - Responsable: [ ] - Fecha: [ ]
- [ ] [Acción 2] - Responsable: [ ] - Fecha: [ ]
```

## 🎓 Programa de Entrenamiento

### Semana 1: Fundamentos McKinsey
- Lectura: "The McKinsey Mind"
- Ejercicio: Descomposición MECE de problemas simples
- Práctica: Crear issue trees para casos de estudio

### Semana 2: Técnicas de Entrevista
- Role-playing: Simulaciones de entrevistas
- Feedback: Grabación y análisis de técnicas
- Mejora: Ajuste de preguntas y escucha activa

### Semana 3: Síntesis y Comunicación
- Ejercicio: Convertir 2h de entrevista en memo de 2 páginas
- Práctica: Presentación ejecutiva (elevator pitch de hallazgos)
- Feedback: Claridad, impacto, llamados a acción

### Semana 4: Integración con IA
- Herramientas: Usar IA para análisis de transcripciones
- Automatización: Templates inteligentes que sugieren preguntas
- Escalabilidad: Sistema para múltiples entrevistas paralelas

## 🤖 Asistencia por IA

### Prompt para análisis de entrevistas:
```
Analiza esta transcripción de entrevista con una PYME de [industria].
Identifica:
1. Los 3 principales pain points mencionados
2. Oportunidades de automatización con IA
3. Métricas mencionadas o implícitas
4. Preocupaciones sobre implementación
5. Recomendaciones específicas para esta empresa

Transcripción: [pegar transcripción]
```

### Prompt para estimación de ROI:
```
Basado en estos hallazgos de entrevista, estima el ROI potencial:
- Problema: [descripción]
- Métrica actual: [valor]
- Meta mejorada: [valor objetivo]
- Frecuencia: [diario/semanal/mensual]
- Costo del problema: [si se mencionó]

Proporciona:
1. Cálculo conservador
2. Cálculo optimista  
3. Supuestos clave
4. Riesgos a considerar
```

## 📈 Métricas de Éxito del Flujo

### Entrenamiento:
- Tiempo promedio de preparación: <2h por entrevista
- Calidad de hallazgos: >80% de hipótesis validadas
- Satisfacción del cliente: NPS >8 en fase de diagnóstico

### Implementación:
- Tasa de conversión entrevista → propuesta: >40%
- Tasa de conversión propuesta → cliente: >25%
- ROI promedio documentado: >3x en primeros 6 meses

---
**Próximo paso:** Crear los templates y checklist específicos, luego programar sesiones de práctica.
```

---
**Estado:** Flujo diseñado, listo para implementación
**Siguiente:** Crear Flujo 2 - Desarrollo de Soluciones