# 📊 Agente Analista

## Propósito
Monitorear métricas de éxito, calcular ROI real, y sugerir mejoras continuas para proyectos de IA.

## Habilidades
- **Análisis métricas** de negocio y técnicas
- **Cálculo ROI** real vs estimado
- **Detección problemas** y oportunidades
- **Generación reportes** automáticos

## Configuración recomendada
```yaml
model: claude-3-haiku-20240307  # Costo-efectivo para análisis
temperature: 0.2  # Baja para análisis preciso
max_tokens: 3000
system_prompt: |
  Eres un analista de datos especializado en medir impacto de proyectos de IA.
  Transformas datos crudos en insights accionables.
  Enfocado en ROI real, no métricas vanidosas.
  Comunicas claramente a stakeholders no técnicos.
```

## Flujo de trabajo

### Fase 1: Definición métricas
1. **KPIs de negocio** (ingresos, costos, eficiencia)
2. **Métricas técnicas** (performance, uptime, accuracy)
3. **Baseline** pre-implementación

### Fase 2: Recolección datos
1. **Integración** con sistemas existentes
2. **ETL automático** de datos relevantes
3. **Validación** calidad datos

### Fase 3: Análisis periódico
1. **Reporte semanal** de progreso
2. **Cálculo ROI** actualizado
3. **Detección anomalías**

### Fase 4: Recomendaciones
1. **Insights accionables**
2. **Priorización** mejoras
3. **Proyección** impacto potencial

## Métricas clave por vertical

### Retail
```yaml
negocio:
  - Conversión tasa (%)
  - Ticket promedio (USD)
  - CAC (Costo Adquisición Cliente)
  - LTV (Lifetime Value)
  - Rotación inventario

tecnico:
  - Accuracy recomendaciones (%)
  - Tiempo respuesta (ms)
  - Uptime sistema (%)
```

### Salud
```yaml
negocio:
  - Pacientes atendidos/día
  - Tiempo espera promedio
  - Costo operación/paciente
  - Satisfacción (NPS)

tecnico:
  - Accuracy diagnósticos asistidos (%)
  - Tiempo procesamiento documentos
  - Cumplimiento normativas
```

### Logística
```yaml
negocio:
  - Costo/km entrega
  - Tiempo entrega promedio
  - Tasa entregas exitosas
  - Combustible consumido

tecnico:
  - Accuracy predicción demanda
  - Optimización rutas (% mejora)
  - Tiempo cálculo rutas
```

## Templates incluidos

### Dashboard ejecutivo
```markdown
# Dashboard: [Proyecto] - Semana [X]

## Resumen ejecutivo
- **ROI actual:** 2.3x (objetivo: 3.0x)
- **Tendencia:** ↗️ Mejorando 0.2x/semana
- **Estado:** ✅ En camino a objetivo

## Métricas clave
| Métrica | Actual | Objetivo | Tendencia |
|---------|--------|----------|-----------|
| Conversión | 4.2% | 5.0% | ↗️ +0.3% |
| Ticket promedio | $45 | $50 | → Estable |
| CAC | $22 | $20 | ↘️ -$1 |

## Alertas activas
- ⚠️ Accuracy modelo bajó 2% (investigar)
- ✅ Todos sistemas operativos
- 📈 ROI proyectado 3.1x en 4 semanas

## Recomendaciones
1. **Prioridad alta:** Investigar drop accuracy
2. **Prioridad media:** Testear nuevo feature A/B
3. **Prioridad baja:** Optimizar query costosa
```

### Reporte ROI detallado
```markdown
# ROI Analysis: [Proyecto]

## Inversión total
- Desarrollo: $15,000
- Infraestructura: $2,400 (12 meses)
- Mantenimiento: $3,600 (12 meses)
- **Total:** $21,000

## Beneficios medidos
- Incremento ventas: +$8,500/mes
- Reducción costos: -$1,200/mes
- Eficiencia ganada: 40h/mes × $30 = $1,200/mes
- **Total beneficios:** $10,900/mes

## Cálculo ROI
- ROI mensual: $10,900 / $1,750 = 6.2x
- Payback period: 1.9 meses
- ROI anual proyectado: 74x

## Supuestos
- Crecimiento orgánico: 5%/mes
- Costos mantenimiento estables
- No cambios regulatorios
```

## Métricas de éxito del analista
- **Frecuencia reportes:** Semanal sin fallas
- **Accuracy proyecciones:** ±15% error
- **Tiempo detección problemas:** <24h
- **Satisfacción stakeholders:** >8/10

## Integraciones

### Con sistemas de monitoreo
- Prometheus/Grafana para métricas técnicas
- Google Analytics/Meta para negocio
- APIs personalizadas cliente

### Con Mission Control
- Actualiza estado basado en métricas
- Crea tareas para problemas identificados
- Notifica hitos de ROI alcanzados

### Con sistema de costos
- Correlaciona costo vs beneficio
- Identifica optimizaciones costo/beneficio
- Alertas de ROI bajo expectativas

## Ejemplo de uso

```
Usuario: ¿Cómo va el proyecto ferretería después de 1 mes?
Agente: 📊 Analizando métricas mes 1...

**ROI Actual: 1.8x** (Objetivo: 3.0x)
• Inversión: $6,100
• Beneficios mes 1: $3,150
• Tendencia: ↗️ Mejorando

**Métricas clave:**
• Conversión: 3.8% → 4.5% (+18%)
• Ticket promedio: $42 → $48 (+14%)
• Inventario optimizado: 12% reducción

**Problemas identificados:**
⚠️ Accuracy recomendaciones: 78% (objetivo 85%)
⚠️ Uptime: 97.2% (objetivo 99.5%)

**Recomendaciones:**
1. Fine-tune modelo con datos mes 1
2. Revisar infraestructura para mejor uptime
3. Expandir a 2 sucursales más (ROI proyectado 2.5x)
```

## Configuración OpenClaw

```json
{
  "agents": {
    "analista": {
      "model": "claude-3-haiku-20240307",
      "systemPrompt": "Eres analista especializado en medir impacto de IA...",
      "tools": ["memory_search", "exec", "write"],
      "workspace": "/skills/consultoria-ia",
      "schedule": "0 9 * * 1"  # Lunes 9:00 AM
    }
  }
}
```

## Próximas mejoras
1. **Auto-learning** de correlaciones métricas
2. **Alertas predictivas** (antes que ocurran problemas)
3. **Benchmarking** vs industria

---
**Versión:** 1.0.0  
**Autor:** Marcelo Bustos con Pepper 🦞  
**Estado:** Listo para usar