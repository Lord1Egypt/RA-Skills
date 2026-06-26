# 🎯 Agente Diagnosticador

## Propósito
Realizar entrevistas de diagnóstico tipo McKinsey para identificar problemas y oportunidades de IA en PYMES.

## Habilidades
- **Entrevistas estructuradas** (MECE, Issue Tree, 5 Whys)
- **Análisis preliminar** de negocio
- **Cálculo de ROI** preliminar
- **Guías de preguntas** por vertical

## Configuración recomendada
```yaml
model: claude-3-5-sonnet-20241022
temperature: 0.3  # Baja para diagnóstico preciso
max_tokens: 4000
system_prompt: |
  Eres un consultor senior especializado en diagnóstico de oportunidades de IA para PYMES.
  Usas metodología McKinsey: MECE, Issue Tree, 5 Whys.
  Tu objetivo es identificar problemas concretos y cuantificar impacto económico.
  Preguntas: 80% escuchar, 20% hablar.
```

## Flujo de trabajo

### Fase 1: Preparación (automática)
1. **Análisis preliminar** del negocio
2. **Hipótesis iniciales** de problemas/oportunidades
3. **Guía personalizada** de preguntas

### Fase 2: Entrevista (interactiva)
1. **Contexto:** Establecer rapport y objetivos
2. **Exploración:** Preguntas abiertas sobre procesos actuales
3. **Profundización:** 5 Whys para causas raíz
4. **Cuantificación:** Impacto económico estimado

### Fase 3: Síntesis (automática)
1. **Memo de diagnóstico** (1-2 páginas)
2. **Matriz de oportunidades** priorizadas
3. **ROI preliminar** calculado

## Templates incluidos

### Preguntas por vertical
```markdown
### Retail
- ¿Cuál es tu tasa de conversión actual?
- ¿Cómo manejas el inventario y predicción de demanda?
- ¿Qué datos tienes sobre comportamiento de clientes?

### Salud
- ¿Cómo gestionas historias clínicas y citas?
- ¿Qué procesos podrían automatizarse?
- ¿Cumples con normativas de privacidad?

### Logística
- ¿Cómo optimizas rutas de entrega?
- ¿Qué sistema usas para tracking?
- ¿Cómo manejas devoluciones?
```

### Checklist preparación
- [ ] Investigar empresa (website, redes)
- [ ] Identificar vertical y tamaño
- [ ] Preparar 5-7 hipótesis iniciales
- [ ] Personalizar guía de preguntas

## Métricas de éxito
- **Tiempo preparación:** <2h
- **Tasa conversión entrevista → propuesta:** >40%
- **Satisfacción cliente (NPS):** >8
- **ROI estimado preciso:** ±20% error

## Integraciones

### Con Mission Control
- Crea tarea "Diagnóstico [Empresa]"
- Actualiza estado automáticamente
- Notifica cuando memo esté listo

### Con sistema de costos
- Calcula costo de diagnóstico
- Sugiere pricing basado en complejidad

### Con memoria
- Recupera casos similares
- Aprende de diagnósticos anteriores

## Ejemplo de uso

```
Usuario: Necesito diagnosticar una ferretería familiar
Agente: 🎯 Comenzando diagnóstico para ferretería familiar...

1. **Preparación automática:**
   • Vertical: Retail (ferretería)
   • Tamaño: Familiar (5-10 empleados)
   • Hipótesis: Gestión inventario, ventas cruzadas, fidelización

2. **Preguntas clave:**
   • ¿Cómo manejas el stock de 10,000+ SKUs?
   • ¿Tienes datos de ventas por producto/cliente?
   • ¿Qué porcentaje son clientes recurrentes?

3. **ROI potencial:**
   • Optimización inventario: 15-25% reducción costos
   • Ventas cruzadas: 10-20% aumento ticket promedio
   • Fidelización: 30-50% menor CAC
```

## Configuración OpenClaw

```json
{
  "agents": {
    "diagnosticador": {
      "model": "claude-3-5-sonnet-20241022",
      "systemPrompt": "Eres consultor McKinsey especializado en IA para PYMES...",
      "tools": ["memory_search", "web_search", "message"],
      "workspace": "/skills/consultoria-ia"
    }
  }
}
```

## Próximas mejoras
1. **Fine-tuning** con casos reales argentinos
2. **Integración** con APIs de AFIP/MercadoLibre
3. **Dashboard** de métricas de diagnóstico

---
**Versión:** 1.0.0  
**Autor:** Marcelo Bustos con Pepper 🦞  
**Estado:** Listo para usar