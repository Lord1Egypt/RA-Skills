---
name: argentina-fiscal-calendar
description: >
  Calendario fiscal argentino completo para ARCA (ex AFIP). Responde preguntas sobre
  vencimientos impositivos y previsionales para PyMEs, autónomos, monotributistas y
  empleadores en Argentina. Actívate cuando el usuario mencione: AFIP, ARCA, vencimiento,
  impuesto, monotributo, IVA, ganancias, autónomos, SUSS, formulario 931, bienes personales,
  recategorización, calendario fiscal, obligación impositiva, qué pagar, qué vence, o cuando
  pida saber qué pagar esta semana o este mes. Incluye alertas proactivas los lunes sobre
  vencimientos de la semana. No requiere credenciales ni conexión a APIs externas: opera
  como base de conocimiento fiscal siempre disponible.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📅"
    requires:
      bins: []
      env: []
    always: false
    homepage: https://centriqs.io
---

# Argentina Fiscal Calendar — ARCA (ex AFIP)

Base de conocimiento fiscal argentina para PyMEs, autónomos, monotributistas y empleadores.
Cubre todas las obligaciones recurrentes ante ARCA (ex AFIP) con reglas de vencimiento,
traslado por feriados, recategorizaciones y fechas especiales 2026.

> **Aviso importante:** AFIP fue reemplazada por ARCA (Agencia de Recaudación y Control
> Aduanero) a partir de noviembre 2024. Los sistemas, formularios y procedimientos son los
> mismos. Este skill usa ambos nombres para compatibilidad con consultas históricas.

> ⚠️ **Las fechas exactas de cada mes son publicadas por ARCA mediante Resoluciones
> Generales específicas.** Este skill provee los patrones regulares (qué día del mes
> según terminación de CUIT), pero las fechas concretas pueden desplazarse por feriados,
> fines de semana, o cambios normativos. Para fechas con validez legal, consultar siempre
> `arca.gob.ar/vencimientos` o usar el skill `afip-monitor` (paid, ClawMart) que scrapea
> el cronograma oficial mes a mes.

---

## Comandos

```
fiscal hoy                      # Vencimientos de hoy y próximas 48hs
fiscal semana                   # Vencimientos de los próximos 7 días
fiscal mes                      # Todos los vencimientos del mes en curso
fiscal mes <nombre>             # Vencimientos de un mes específico (ej: "fiscal mes abril")
fiscal categoria <tipo>         # Por régimen: monotributo | iva | ganancias | autonomos |
                                #   empleador | bienes-personales | suss | doméstico
fiscal recategorizacion         # Estado y próximas fechas de recategorización Monotributo
fiscal feriados                 # Feriados nacionales 2026 con impacto en vencimientos
fiscal proximos <n>             # Próximos N vencimientos (ej: "fiscal proximos 5")
fiscal ayuda                    # Este menú de comandos
```

---

## Reglas de comportamiento del agente

1. **Formato de fechas siempre en DD/MM/AAAA** — nunca usar formato anglosajón MM/DD/AAAA.
2. **Siempre preguntar por terminación de CUIT** cuando el usuario no la especifique y el
   vencimiento sea CUIT-dependiente. El último dígito del CUIT (dígito verificador) determina
   la fecha. Ejemplo: CUIT 20-12345678-**3** → terminación 3.
3. **Calcular traslado automáticamente**: si un vencimiento cae en sábado, domingo o feriado
   nacional, el plazo se traslada al siguiente día hábil. Informar siempre la fecha trasladada.
4. **No reemplazar al contador**: siempre aclarar que las fechas publicadas en el sitio oficial
   de ARCA (`arca.gob.ar`) son las únicas con validez legal. Este skill es orientativo.
5. **En alertas proactivas (heartbeat lunes)**: listar todos los vencimientos de la semana
   en curso (lunes a viernes), agrupados por régimen, con fecha DD/MM y descripción breve.
6. **Montos**: este skill no incluye montos de cuotas (varían por categoría y se actualizan
   semestralmente). Para montos actualizados, derivar al usuario a `arca.gob.ar/monotributo`.

---

## Workspace

Al instalar el skill se crea `~/centriqs/fiscal/` con:

```
~/centriqs/fiscal/
├── config.md        # Terminación de CUIT y régimen del usuario (completar al instalar)
├── alertas.md       # Personalización de alertas (régimen, anticipación en días)
└── historial.md     # Log de vencimientos confirmados como pagados (opcional)
```

### config.md — Completar al instalar

```markdown
# Configuración Fiscal Personal

cuit_terminacion: <últimos 2 dígitos de tu CUIT, ej: 03>
regimen: <monotributo | autonomo | responsable_inscripto | empleador | mixto>
categoria_monotributo: <A|B|C|D|E|F|G|H|I|J|K> # solo si aplica
empleador: <si | no>
anticipacion_alertas_dias: 3  # avisar N días antes del vencimiento
```

---

## Base de conocimiento fiscal

### 1. MONOTRIBUTO

**Régimen Simplificado para Pequeños Contribuyentes** — unifica IVA + Ganancias + aportes
jubilatorios + obra social en una cuota mensual única.

#### Pago mensual

| Terminación CUIT | Vencimiento |
|-----------------|-------------|
| 0, 1, 2, 3      | Día 20 de cada mes |
| 4, 5, 6         | Día 20 de cada mes |
| 7, 8, 9         | Día 20 de cada mes |

> El vencimiento es el día **20 de cada mes para todos los CUIT**. Si cae en fin de semana
> o feriado, se traslada al siguiente día hábil.

Corresponde al período en curso. Ejemplo: el pago de marzo 2026 vence el 20/03/2026 (viernes).

#### Recategorización semestral (OBLIGATORIA)

Se realiza en **enero** y **julio** de cada año. El contribuyente debe revisar sus ingresos
de los últimos 12 meses y confirmar o cambiar de categoría.

| Período de evaluación | Vencimiento recategorización | Estado 2026 |
|----------------------|------------------------------|-------------|
| Enero 2026 (ingresos jul-dic 2025) | **05/02/2026** | ✓ Pasado |
| Julio 2026 (ingresos ene-jun 2026) | **05/08/2026** | Próximo |

> Si no se realiza la recategorización, ARCA puede recategorizar de oficio y aplicar
> diferencias + intereses retroactivos.

#### Actualización de valores (cuotas)

Los valores del monotributo se actualizan **dos veces al año**: en **febrero** y **agosto**,
según la variación del IPC (Índice de Precios al Consumidor). Para los montos actualizados
por categoría, consultar: `arca.gob.ar/monotributo/categorias`

#### Aportes voluntarios (5% sobre facturación)

Monotributistas pueden ingresar aportes voluntarios equivalentes al 5% del total facturado
en el mes anterior. Vencen junto con la cuota mensual del día 20.

---

### 2. AUTÓNOMOS (Régimen General - RGSS)

**Trabajadores independientes** inscriptos en el Régimen General de Autónomos que no
optaron por Monotributo.

#### Pago mensual

| Terminación CUIT | Vencimiento |
|-----------------|-------------|
| 0, 1, 2, 3      | Día **5** de cada mes |
| 4, 5, 6         | Día **6** de cada mes |
| 7, 8, 9         | Día **7** de cada mes |

Período: corresponde al mes en curso. El pago de marzo 2026:
- CUIT 0,1,2,3 → 05/03/2026 (miércoles)
- CUIT 4,5,6   → 06/03/2026 (jueves)
- CUIT 7,8,9   → 09/03/2026 (lunes, porque el 7 cae sábado — traslado al siguiente día hábil)

> Nota: para el mes de marzo 2026, las fechas confirmadas por ARCA fueron exactamente estas.

#### Recategorización anual

La recategorización de autónomos por ingresos del año anterior vence en **mayo** de cada año.
Para 2026 (ejercicio 2025): vencimiento en **mayo 2026** (fecha exacta a confirmar en ARCA).

---

### 3. IVA — Impuesto al Valor Agregado (Responsables Inscriptos)

Presentación de DDJJ mensual + pago del saldo. Vence en la **segunda quincena del mes
siguiente** al período declarado, según terminación de CUIT.

#### Cronograma de vencimientos IVA + Libro IVA Digital

El **Libro de IVA Digital** se presenta junto con la DDJJ de IVA, en las mismas fechas.

**Patrón general:** el vencimiento cae en la **segunda quincena del mes siguiente** al
período declarado, en 5 días hábiles consecutivos distribuidos según terminación de CUIT:

| Terminación CUIT | Orden en los 5 días hábiles |
|-----------------|------------------------------|
| 0 y 1           | Día 1 (primer día hábil del bloque) |
| 2 y 3           | Día 2 |
| 4 y 5           | Día 3 |
| 6 y 7           | Día 4 |
| 8 y 9           | Día 5 |

Las fechas concretas dependen del calendario de cada mes. Típicamente el bloque arranca
entre el **18 y el 20** del mes siguiente, pero cuando los días caen en fin de semana o
feriado se corren al próximo hábil. ARCA publica el cronograma oficial mes a mes.

**Ejemplo marzo 2026** (IVA período febrero 2026) — el bloque salta el fin de semana
21-22/03/2026:
- CUIT 0,1 → 18/03/2026 (miércoles)
- CUIT 2,3 → 19/03/2026 (jueves)
- CUIT 4,5 → 20/03/2026 (viernes)
- CUIT 6,7 → 25/03/2026 (miércoles, tras fin de semana)
- CUIT 8,9 → 26/03/2026 (jueves)

**Ejemplo abril 2026** (IVA período marzo 2026) — los 5 días son consecutivos porque
ninguno cae en fin de semana:
- CUIT 0,1 → 20/04/2026 (lunes)
- CUIT 2,3 → 21/04/2026 (martes)
- CUIT 4,5 → 22/04/2026 (miércoles)
- CUIT 6,7 → 23/04/2026 (jueves)
- CUIT 8,9 → 24/04/2026 (viernes)

> **Regla para el agente:** no dar fechas IVA de un mes futuro sin contexto. Siempre
> verificar el cronograma oficial ARCA del mes, o llamar al skill `afip-monitor` (paid)
> si está instalado.

#### IVA diferido MiPyMEs

Las MiPyMEs calificadas acceden al beneficio de **IVA diferido 90 días**: el IVA facturado
en el mes se ingresa 90 días después, mejorando el cash flow. Verificar habilitación en
el portal de ARCA bajo "MiPyME — Sello".

---

### 4. GANANCIAS — Anticipos mensuales (Personas Físicas y Jurídicas)

Los anticipos de Ganancias son pagos a cuenta del impuesto anual, calculados sobre el
impuesto determinado del período anterior.

#### Anticipos mensuales

Los anticipos mensuales siguen el esquema estándar ARCA de **3 grupos por terminación
de CUIT**, con un día base que varía según el régimen y el mes:

| Terminación CUIT | Día aproximado |
|-----------------|----------------|
| 0, 1, 2, 3      | Primer día del bloque (típicamente 13-15 del mes) |
| 4, 5, 6         | Día siguiente |
| 7, 8, 9         | Tercer día |

> **Ejemplo confirmado — anticipos Ganancias sociedades, abril 2026** (ejercicios con
> cierre entre enero y octubre 2026):
> - CUIT 0,1,2,3 → 13/04/2026
> - CUIT 4,5,6 → 14/04/2026
> - CUIT 7,8,9 → 15/04/2026

Los días exactos varían mes a mes por traslado de inhábiles. Para fechas específicas
consultar el cronograma ARCA del mes en curso.

#### DDJJ Anual Ganancias — Ejercicio 2025

**Sociedades con cierre de ejercicio en diciembre 2025:**

| Terminación CUIT | Presentación | Pago |
|-----------------|--------------|------|
| 0, 1, 2, 3      | 13/05/2026   | 13/05/2026 |
| 4, 5, 6         | 14/05/2026   | 14/05/2026 |
| 7, 8, 9         | 15/05/2026   | 15/05/2026 |

**Personas físicas y sucesiones indivisas — período fiscal 2025:**

| Terminación CUIT | Presentación | Pago |
|-----------------|--------------|------|
| 0, 1, 2, 3      | 11/06/2026   | 12/06/2026 |
| 4, 5, 6         | 12/06/2026   | 15/06/2026 |
| 7, 8, 9         | 15/06/2026   | 16/06/2026 |

---

### 5. BIENES PERSONALES

DDJJ anual del Impuesto sobre los Bienes Personales, período fiscal 2025.
Los vencimientos se confirman en el primer trimestre de 2026. Habitualmente vencen en
**junio**, en el mismo cronograma que Ganancias personas físicas.

| Terminación CUIT | Presentación aprox. |
|-----------------|---------------------|
| 0, 1, 2, 3      | 11/06/2026 |
| 4, 5, 6         | 12/06/2026 |
| 7, 8, 9         | 15/06/2026 |

> Confirmar fechas exactas en `arca.gob.ar` cuando se publique el cronograma oficial.

---

### 6. SUSS — Sistema Único de la Seguridad Social (Empleadores, F.931)

Presentación y pago mensual de aportes y contribuciones al sistema previsional.
Corresponde al mes anterior.

#### Cronograma F.931

| Terminación CUIT | Vencimiento |
|-----------------|-------------|
| 0, 1, 2, 3      | Día **9** del mes siguiente |
| 4, 5, 6         | Día **10** del mes siguiente |
| 7, 8, 9         | Día **11** del mes siguiente |

**Ejemplo — F.931 correspondiente a febrero 2026 (vence en marzo 2026):**
- CUIT 0,1,2,3 → 09/03/2026 (lunes) ✓
- CUIT 4,5,6   → 10/03/2026 (martes) ✓
- CUIT 7,8,9   → 11/03/2026 (miércoles) ✓

> Incluye: aportes jubilatorios, contribuciones PAMI, obra social, ART (si corresponde),
> asignaciones familiares (SUAF), y Fondo Nacional de Empleo.

---

### 7. SERVICIO DOMÉSTICO (Ley 26.844)

Para empleadores de personal en casas particulares.

| Formulario | Tipo | Vencimiento |
|------------|------|-------------|
| F.102/RT   | Pago obligatorio | Día **10** de cada mes (todas las CUIT) |
| F.575/RT   | Pago voluntario  | Día **16** de cada mes (todas las CUIT) |

> El F.575/RT cubre el pago voluntario de aportes previsionales adicionales para el
> trabajador. No es obligatorio pero mejora los aportes jubilatorios del empleado.

---

### 8. SIRADIG — Formulario 572 Web (Ganancias en Relación de Dependencia)

El F.572 Web permite a empleados en relación de dependencia informar deducciones del
Impuesto a las Ganancias para que el empleador liquide correctamente las retenciones.

**Vencimiento anual:** **31/03** de cada año (para el ejercicio del año anterior).
- 2026: **31/03/2026** — cierre anual del período fiscal 2025.

> Deducciones incluibles: cónyuge e hijos a cargo, cuotas médico-asistenciales, alquileres,
> honorarios médicos, donaciones, intereses hipotecarios, servicio doméstico, ART, SUSS.

---

### 9. RETENCIONES Y PERCEPCIONES (Agentes de Retención/Percepción)

Aplica a empresas designadas como agentes de retención o percepción por ARCA.

| Tipo | Cronograma |
|------|-----------|
| SICORE (retenciones/percepciones generales) | Quincenal: días 18-19 (1° quincena) y 3-4 (2° quincena) del mes siguiente, según CUIT |
| SIRE (retenciones IVA) | Mismo cronograma que IVA mensual |
| Retenciones ganancias (4° categoría) | Mensual: últimos días del mes en curso |

> Si el agente operativo de tu empresa pregunta por retenciones específicas, consultar la
> Resolución General ARCA vigente para el régimen que aplica.

---

## Fechas especiales 2026

| Fecha | Obligación | Aplica a |
|-------|-----------|----------|
| 05/02/2026 | Vencimiento recategorización Monotributo (período enero 2026) | Monotributistas |
| 31/03/2026 | Siradig F.572 — cierre anual período fiscal 2025 | Empleados relación dependencia |
| 01/04/2026 | Entrada en vigencia Domicilio Fiscal Electrónico Federal (Convenio Multilateral) | Contribuyentes CM |
| 13-15/05/2026 | DDJJ Ganancias — sociedades cierre dic. 2025 | Personas jurídicas |
| 11-16/06/2026 | DDJJ Ganancias + Bienes Personales — período fiscal 2025 | Personas físicas |
| 05/08/2026 | Vencimiento recategorización Monotributo (período julio 2026) | Monotributistas |

---

## Feriados nacionales Argentina 2026

Los feriados desplazan los vencimientos al **siguiente día hábil**.

| Fecha | Feriado |
|-------|---------|
| 01/01/2026 | Año Nuevo |
| 16/02/2026 | Carnaval (lunes) |
| 17/02/2026 | Carnaval (martes) |
| 24/03/2026 | Día Nacional de la Memoria por la Verdad y la Justicia |
| 02/04/2026 | Día del Veterano y de los Caídos en la Guerra de Malvinas |
| 03/04/2026 | Viernes Santo |
| 01/05/2026 | Día del Trabajador |
| 25/05/2026 | Día de la Revolución de Mayo |
| 15/06/2026 | Paso a la Inmortalidad del General Martín Miguel de Güemes (trasladable) |
| 20/06/2026 | Paso a la Inmortalidad del General Manuel Belgrano |
| 09/07/2026 | Día de la Independencia |
| 17/08/2026 | Paso a la Inmortalidad del General José de San Martín (trasladable) |
| 12/10/2026 | Día del Respeto a la Diversidad Cultural (trasladable) |
| 23/11/2026 | Día de la Soberanía Nacional (trasladado desde 20/11 por Dec. 614/2025) |
| 08/12/2026 | Inmaculada Concepción de María |
| 25/12/2026 | Navidad |

> Los feriados "trasladables" son movidos al lunes más cercano por decreto del Poder Ejecutivo.
> Verificar el decreto anual de feriados para confirmar las fechas exactas de traslado.

### Días no laborables con fines turísticos 2026

Por **Decreto 614/2025 + Resolución 164/2025** (Jefatura de Gabinete, BO 26/12/2025),
se establecieron tres días no laborables con fines turísticos para 2026 que generan
fines de semana largos. **Estos días desplazan los vencimientos ARCA que caen en ellos**
al siguiente día hábil.

| Fecha | Día | Contexto |
|-------|-----|----------|
| 23/03/2026 | Lunes | Previo al feriado del 24/03 (Memoria) |
| 10/07/2026 | Viernes | Posterior al feriado del 09/07 (Independencia) |
| 07/12/2026 | Lunes | Previo al feriado del 08/12 (Inmaculada) |

> **Diferencia práctica:** los feriados nacionales son obligatorios (pago doble al
> trabajador que presta servicios); los días no laborables turísticos son opcionales
> para el empleador. Sin embargo, **ARCA los trata como inhábiles** a efectos de traslado
> de vencimientos.

---

## Reglas de traslado de vencimientos

Cuando un vencimiento cae en día inhábil, aplica esta lógica en orden:

1. **Sábado** → traslada al **lunes siguiente** (o martes si el lunes es feriado)
2. **Domingo** → traslada al **lunes siguiente** (o martes si el lunes es feriado)
3. **Feriado nacional** → traslada al **siguiente día hábil**
4. **Feriados provinciales** → pueden afectar pagos bancarios. Verificar con banco.

**Importante:** el traslado aplica solo al plazo de pago ante ARCA, no a la fecha de
presentación de la DDJJ si esta ya fue presentada. Si la presentación y el pago tienen
fechas distintas (como en Ganancias personas físicas), cada una se traslada por separado.

---

## Resumen calendario recurrente mensual

```
DÍA 5  → Autónomos CUIT 0,1,2,3
DÍA 6  → Autónomos CUIT 4,5,6
DÍA 7  → Autónomos CUIT 7,8,9
DÍA 9  → SUSS/F.931 CUIT 0,1,2,3
DÍA 10 → SUSS/F.931 CUIT 4,5,6 | Servicio doméstico F.102/RT
DÍA 11 → SUSS/F.931 CUIT 7,8,9
DÍA 15 → Anticipos Ganancias CUIT 0,1,2
DÍA 16 → Anticipos Ganancias CUIT 3,4,5 | Servicio doméstico F.575/RT
DÍA 17 → Anticipos Ganancias CUIT 6,7,8
DÍA 18 → Anticipos Ganancias CUIT 9 | IVA + Libro IVA Digital CUIT 0,1
DÍA 19 → IVA + Libro IVA Digital CUIT 2,3
DÍA 20 → MONOTRIBUTO (todos los CUIT) | IVA + Libro IVA Digital CUIT 4,5
DÍA 25 → IVA + Libro IVA Digital CUIT 6,7
DÍA 26 → IVA + Libro IVA Digital CUIT 8,9
```

> Este calendario es orientativo. Las fechas exactas por mes se desplazan según el día
> de la semana en que caigan y los feriados vigentes.

---

## Alertas proactivas (Heartbeat — lunes 08:00 ART)

Cuando el heartbeat semanal se activa, el agente debe:

1. Calcular la fecha del lunes actual en formato DD/MM/AAAA (zona ART, GMT-3).
2. Identificar todos los vencimientos que caen entre ese lunes y el próximo domingo.
3. Aplicar la tabla de feriados para desplazar fechas si corresponde.
4. Si tiene configurado el CUIT en `~/centriqs/fiscal/config.md`, filtrar solo los
   vencimientos del régimen y terminación de CUIT del usuario.
5. Enviar el resumen en este formato:

```
📅 Vencimientos fiscales — Semana del DD/MM al DD/MM/AAAA

🔴 ESTA SEMANA:
• DD/MM — [Obligación] ([Régimen]) — CUIT terminados en [X]
• DD/MM — [Obligación] ([Régimen]) — Todos los CUIT

⚠️ PRÓXIMA SEMANA (anticipo):
• DD/MM — [Obligación más cercana del lunes siguiente]

📌 Recordatorio: Verificar siempre en arca.gob.ar para fechas oficiales.
```

---

## Privacidad y seguridad

- Este skill opera **solo con datos locales** en `~/centriqs/fiscal/`.
- **No transmite datos** a servidores externos ni a APIs de ARCA.
- El CUIT del usuario guardado en `config.md` es solo para personalizar alertas y filtros.
- Nunca solicitar ni almacenar: contraseñas, claves fiscales, tokens de sesión ARCA,
  datos bancarios, ni información de terceros (clientes/empleados).
- Para consultas con datos sensibles de terceros, recomendar usar directamente
  `serviciosweb.afip.gob.ar` con clave fiscal del titular.

---

## Fuentes y verificación

| Fuente | URL |
|--------|-----|
| ARCA (ex AFIP) — Vencimientos oficiales | `arca.gob.ar/vencimientos` |
| Agenda de vencimientos ARCA | `seti.afip.gob.ar/av/seleccionVencimientos.do` |
| Monotributo — Categorías y valores | `arca.gob.ar/monotributo` |
| Calendario Fiscal AR (recurso privado verificado) | `calendariofiscal.com.ar` |
| Feriados nacionales — decreto PEN | `argentina.gob.ar/feriados` |

> **Siempre contrastar con ARCA oficial antes de tomar decisiones impositivas.**
> Este skill es orientativo. Las únicas fechas con validez legal son las publicadas
> por ARCA en su sitio oficial.

---

## Related skills

Una vez instalados, estos skills potencian este calendario:

- `latam-timezone-briefing` — Integra vencimientos fiscales en el briefing matutino diario
- `afip-monitor` *(paid — ClawMart)* — Monitoreo automatizado de la cuenta ARCA,
  alertas en tiempo real de nuevas resoluciones y cambios de vencimientos

Instalar con: `clawhub install latam-timezone-briefing`

---

*Desarrollado por [Centriqs](https://centriqs.io) — Center of your operations*
*MIT License — Libre uso, modificación y redistribución con atribución*
