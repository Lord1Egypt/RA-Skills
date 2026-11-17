# Pool Semanal — Templates de razones por tipo de activo

> Referencial cargado por la skill `calendarizador-urgencias-formula100k`.
> Para cada activo del producto que el usuario marque en el Bloque C del brief,
> usa estas plantillas como base y adáptalas al lenguaje + contexto específico.

---

## Cómo se usa este archivo

1. Lee los activos seleccionados en el Bloque C
2. Para cada activo, toma 2-4 razones de su sección
3. Reemplaza `{{...}}` con datos del brief (nombre del producto, día de la sesión, etc.)
4. Asegúrate de que la razón sea VERIFICABLE para ese producto en particular
5. Si una plantilla menciona un dato que el usuario no tiene, NO la incluyas

**Objetivo:** terminar con un pool de 15-25 razones rotativas. Si una semana del mes no
tiene evento estacional fuerte, se rota una razón del pool.

---

## 1. SESIONES EN VIVO RECURRENTES

**Tipo de escasez:** Tiempo (cap de la sesión)
**Gatillo:** Urgencia táctica + Escasez cruda

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Llegar a la sesión de esta semana | Lunes/martes | "Si entras antes del {{día}}, llegas a la sesión de {{día_sesion}} a las {{hora}}." |
| Cap operativo de la sesión | Cuando hay >X registradas | "La sesión de {{día_sesion}} tiene cupo de {{N}}. Quedan {{X}} lugares — después se graba pero no respondo en vivo." |
| Sesión temática especial | Una vez al mes | "Esta semana es la sesión de {{tema_mes}}. Es 1 vez al año. Si entras hoy, alcanzas." |
| Sesión con invitado externo | Cuando hay guest | "{{nombre_guest}} viene en vivo el {{fecha}}. No queda grabada. Si no estás dentro, te lo pierdes." |

---

## 2. COHORTES CON ONBOARDING SINCRONIZADO

**Tipo de escasez:** Tiempo (deadline real de la cohorte)
**Gatillo:** Urgencia táctica + Aversión a la pérdida

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Cierre de cohorte mensual | Días -7, -3, -1 del cierre | "Cohorte de {{mes}} cierra el {{fecha}}. Después arrancas con la del {{mes_siguiente}} — un mes de comunidad que no recuperas." |
| Bienvenida en vivo sincronizada | -2 días antes | "El {{fecha_kickoff}} hago el live de bienvenida a la cohorte. Solo las que entran antes participan en vivo." |
| Material exclusivo de cohorte | Después del cierre | "La cohorte de {{mes}} recibió {{material}}. Esto no se reparte a las que entran después." |
| Cap de cohorte | Si hay límite real | "Esta cohorte tiene {{N}} plazas. Quedan {{X}}." |

---

## 3. COMUNIDAD ACTIVA (Skool / Discord / Telegram / FB / Slack)

**Tipo de escasez:** Social + Contexto
**Gatillo:** Prueba social + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Conversación en vivo de la semana | Cualquier momento | "Esta semana en la comunidad {{N}} personas ya están debatiendo {{tema}}. Te lo pierdes desde afuera." |
| Hot seat / auditoría de miembras | Cuando hay sesión | "El {{día}} auditamos en vivo el {{activo}} de una miembra. Si entras hoy, llevas el tuyo." |
| Casos compartidos en privado | Genérico | "Las miembras comparten {{tipo_caso}} que NO se publican afuera." |
| Networking entre miembras | Genérico | "Ya hay {{N}} miembras del mismo nicho que tú dentro. La sala donde se conecta esa gente está cerrada." |

---

## 4. DROPS DE MÓDULOS / CONTENIDO NUEVO

**Tipo de escasez:** Tiempo + Bonus
**Gatillo:** Aversión a la pérdida + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Drop de módulo nuevo este mes | Semana del drop | "Este mes sale el módulo de {{tema}}. Las miembras activas lo reciben GRATIS. Si entras hoy, te llega." |
| Bonus por entrar antes del drop | -7 días | "El módulo de {{tema}} se lanza el {{fecha}}. Después se suma al precio del programa. Si entras antes, lo recibes incluido." |
| Acceso anticipado a beta | Cuando hay beta | "10 miembras tendrán acceso anticipado a {{producto_nuevo}} antes de lanzarlo. Para entrar a esa lista, hay que estar dentro este mes." |

---

## 5. APPS / HERRAMIENTAS EXCLUSIVAS (no se venden sueltas)

**Tipo de escasez:** Contexto / Exclusividad
**Gatillo:** Exclusividad + Aversión a la pérdida

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Acceso único | Evergreen | "{{nombre_app}} no se vende suelta. {{nombre_producto}} es la única puerta." |
| Comparación de costo | Cuando el producto vale > precio | "Por separado, {{nombre_app}} costaría {{$X}}. Adentro de {{producto}} entra incluida." |
| Actualizaciones automáticas | Genérico | "Las miembras de {{producto}} reciben todas las actualizaciones de {{app}} sin pagar extra." |

---

## 6. BONOS / SESIONES 1-ON-1

**Tipo de escasez:** Cantidad (cap operativo real)
**Gatillo:** Escasez cruda + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Sesión 1:1 con el creador / experto | Si aplica al nivel | "Las primeras {{N}} que entren este mes reciben una sesión 1-on-1 conmigo. Quedan {{X}}." |
| Auditoría personalizada | Genérico | "Si entras antes del {{fecha}}, te audito {{activo}} en privado. Después es solo grupal." |
| Bonus por pago anual | Cuando aplica | "Las que eligen anual reciben {{bonus}} sin costo extra. Las mensuales no." |

---

## 7. WORKSHOPS / LIVES TEMÁTICOS PUNTUALES

**Tipo de escasez:** Tiempo
**Gatillo:** Urgencia táctica + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Workshop del mes | Semana previa | "El {{fecha}} hago workshop de {{tema}}. Es 1 vez al año. Solo miembros activas." |
| Live de Q4 / planeación | Trimestral | "El {{fecha}} hacemos planeación de {{trimestre}} en vivo. Si entras antes, llegas." |
| Masterclass de objeción específica | Cuando hay ola | "Esta semana hay masterclass de {{tema_caliente}}. Solo se guarda 30 días." |

---

## 8. GARANTÍA

**Tipo de escasez:** Tiempo (de la garantía)
**Gatillo:** Aversión a la pérdida invertida (reducción de riesgo)

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Garantía de prueba | Evergreen | "Tienes {{N}} días para probar. Si no es lo que esperabas, devuelvo el 100%." |
| Garantía de resultado | Si aplica | "Si haces {{X}} y no llegas a {{Y}}, te devuelvo o te trabajo gratis hasta lograrlo." |
| Recordatorio del bajo riesgo | Cierre de campaña | "Por {{$precio}} y {{N}} días de garantía, el riesgo es del 0%. La pregunta es: ¿qué pierdes si NO entras?" |

> **Importante:** una garantía sin uso real NO es activo de urgencia — es ruido. Solo
> usar si está respaldada por proceso documentado.

---

## 9. ACCESO A EQUIPO / CONSULTORES / MENTORES

**Tipo de escasez:** Cantidad (horas finitas de cada consultora)
**Gatillo:** Escasez cruda + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Cap de horas del equipo | Cuando se llena | "Mi equipo de {{N}} consultoras tiene cupo limitado de auditorías cada mes. Las primeras X que entren se llevan los slots." |
| Mentor invitado | Trimestral | "Este trimestre tenemos a {{nombre_mentor}} dando {{tipo_sesión}}. Solo miembras activas durante esas semanas acceden." |

---

## 10. CASOS DE ÉXITO PÚBLICOS

**Tipo de escasez:** Social
**Gatillo:** Prueba social

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Caso reciente | Cuando hay testimonio fresco | "{{nombre_miembra}} cerró su primer cliente esta semana después de {{N}} semanas dentro. Captura en la comunidad." |
| Acumulado del mes | Fin de mes | "Este mes {{N}} miembras facturaron por primera vez. Yo no las conozco antes — la comunidad las sostiene." |
| Cohorte específica | Trimestral | "Las miembras de {{cohorte_X}} ya cerraron juntas {{$total}}. Si entras hoy, vas con la siguiente cohorte." |

---

## 11. HOT SEAT / AUDITORÍAS PERSONALIZADAS

**Tipo de escasez:** Tiempo (slot semanal)
**Gatillo:** Urgencia táctica + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Hot seat de la semana | Lunes | "Esta semana yo audito {{activo}} en vivo a {{N}} miembras. Te toca si te postulas adentro." |
| Auditoría rotativa | Mensual | "Audito 1 perfil/oferta/comunidad por semana. Si entras hoy, estás en la fila." |

---

## 12. EVENTOS FÍSICOS / RETIROS

**Tipo de escasez:** Cantidad (plazas físicas) + Tiempo (fecha cerrada)
**Gatillo:** Escasez cruda + Exclusividad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Retiro/evento anual | -3 meses | "El retiro de {{ciudad}} {{fecha}} tiene {{N}} plazas. Solo miembros activas pueden aplicar. Quedan {{X}}." |
| Pre-venta de tickets | Genérico | "Las miembras de {{producto}} acceden a tickets antes del público general." |

---

## 13. CERTIFICACIÓN / TÍTULO EMITIDO

**Tipo de escasez:** Contexto + cohorte
**Gatillo:** Exclusividad + Identidad

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Cohorte cerrada para certificación | -7 días | "La certificación de {{nombre}} solo se entrega a las cohortes que arrancan el día 1. Si entras tarde, esperas la próxima." |
| Acreditación con valor en mercado | Evergreen | "El título de {{certificación}} ya lo aceptan {{tipo_clientes/empresas}}. Si entras hoy, lo recibes al cerrar la cohorte." |

---

## 14. PRECIO ESCALONADO REAL

**Tipo de escasez:** Tiempo + Cantidad
**Gatillo:** Aversión a la pérdida + Urgencia táctica

| Razón | Cuándo activarla | Copy modelo |
|---|---|---|
| Subida programada de precio | -14, -7, -3, -1 día | "Las próximas {{N}} entradas pagan {{$precio_actual}}. Después sube a {{$precio_nuevo}} — y SE QUEDA." |
| Subida por cohorte | Al cerrar cohorte | "La cohorte de {{mes}} fue la última a {{$precio}}. La de {{mes_siguiente}} ya entra con el nuevo." |

> ⚠️ Si dices que sube, DEBE subir. Y quedarse arriba 30+ días. Sin esto, mata la marca.

---

## Reglas para usar este pool

1. **Mínimo 1 razón por activo seleccionado.** Si el usuario marcó 6 activos, salen mínimo 6 razones — idealmente 15-25.
2. **Distribución por gatillo:** intentar que el pool tenga al menos 1 razón de CADA uno de los 5 gatillos. Si falta alguno, hueco visible en la matriz.
3. **Cadencia de uso:** las razones de TIEMPO (sesiones, cohortes) se usan en TODA la semana del evento. Las EVERGREEN (apps exclusivas, garantía) sirven de relleno en semanas sin evento.
4. **Una razón nunca cubre dos urgencias simultáneas.** Si esta semana cierra cohorte Y hay drop de módulo, elige UNA y guarda la otra para la siguiente.
5. **Si el activo NO es verificable** (ej: el usuario dice "tengo comunidad" pero no responde por días), no genera razón asociada — márcalo en pendientes.
