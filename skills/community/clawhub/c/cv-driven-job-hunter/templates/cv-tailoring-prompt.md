# CV tailoring — guía para el agente

Cuando el usuario decide postular a una oferta concreta, el agente arma una versión adaptada del CV. Esta guía define **qué se puede y qué no se puede tocar**.

## Lo que SÍ podés hacer

1. **Reordenar bullets** dentro de cada rol — los más relevantes a los requisitos del posting van arriba.

2. **Reordenar la sección de skills** — destacá primero las que el posting menciona.

3. **Reescribir el resumen/summary** — adaptá las primeras 2-3 líneas para que mencionen el rol específico y reflejen el lenguaje del posting (ej: si el posting dice "distributed systems engineer", y el CV original dice "backend engineer", podés ajustar — siempre que la experiencia descrita realmente cubra distributed systems).

4. **Renombrar títulos de roles previos** dentro del rango razonable de la realidad — ej: si fuiste "Senior Software Engineer" pero tu trabajo era de Tech Lead, podés escribir "Senior Software Engineer — Tech Lead" en el CV. Pero NUNCA inflar de Senior a Staff sin que la experiencia lo respalde.

5. **Expandir bullets** que estaban cortos con detalle ya conocido del rol — si tenés notas separadas con métricas que no estaban en el CV pero que viste en el `profile.json` o que el usuario te confirmó, agregalas.

6. **Cambiar el énfasis de tecnologías**: si en el rol X usaste 8 tecnologías y la oferta menciona 3, mencioná esas 3 prominentemente y el resto en una línea de "Stack: ...".

## Lo que NO podés hacer

1. **Inventar experiencia que no existe.** Cero. Ni "uno-año-y-medio-pero-mostrémoslo-como-tres".

2. **Inventar métricas.** Si no hay número en la fuente, no lo pongas. Mejor un bullet sin número que un número falso.

3. **Cambiar fechas** para parecer más senior o ocultar gaps. Si hay un gap, manejalo en la cover letter, no escondiéndolo en el CV.

4. **Atribuir trabajo de equipo a la persona individual** sin marcar el alcance. "Liderar la migración a Kubernetes" cuando fuiste uno de cinco engineers contribuyendo es un problema en la entrevista técnica.

5. **Usar tecnologías como skills si solo fueron exposición.** Si tocó Kafka una vez en producción durante 2 semanas, no es un skill. Sí podés mencionarlo en el contexto del rol como "exposure to Kafka", pero no en la sección de skills principales.

6. **Cambiar la lengua del original sin avisar.** Si el CV está en español y el posting es en inglés, hacele al usuario una versión en inglés explícitamente, no un Frankenstein bilingüe.

## Outputs

Por cada postulación generá:

- `data/applications/{slug}/cv-tailored.md` — versión markdown editable del CV adaptado
- `data/applications/{slug}/changes.md` — diff humano de qué cambiaste vs el CV original (3-5 bullets)
- `data/applications/{slug}/cover-letter.md` — cover usando `templates/cover-letter.md`

Mostrale al usuario `changes.md` primero para que apruebe o pida ajustes antes de mostrarle el CV completo. Es más rápido iterar sobre el diff que sobre el CV entero.

## Cuando exportar

El CV final probablemente necesite estar en PDF. El agente NO genera PDFs automáticamente — le pasa el markdown al usuario y le sugiere:

1. Pegar en su template de Word/Pages/Google Docs habitual y exportar a PDF
2. O usar `pandoc cv-tailored.md -o cv.pdf` si tiene pandoc + LaTeX
3. O herramientas tipo `resume.lol`, `flowcv`, `rxresume` que aceptan markdown

Esto deja el control de presentación visual al usuario, donde debe estar.
