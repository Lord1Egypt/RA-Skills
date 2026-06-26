# Base de Conocimiento: Diccionario de Patrones (Español)

Este documento detalla los 20 patrones específicos de escritura detectados en español. Utiliza estas definiciones para entender por qué un texto ha sido marcado y cómo transformarlo en contenido con voz humana.

| ID | Nombre | Descripción Técnica | ¿Por qué es una señal de IA? | Fix (Cómo arreglarlo) |
|:---|:---|:---|:---|:---|
| **PatternES-01** | Gerundio encadenado | Dos o más gerundios en la misma frase. | Genera una sintaxis monótona y arrastrada, típica de traducciones o generación recursiva. | Reescribir usando verbos finitos y cláusulas separadas. |
| **PatternES-02** | Apertura con contexto vago | Frases como "En el mundo actual" o "En la era digital". | Los LLMs usan marcos contextuales genéricos para "introducir" temas sin ir al grano. | Eliminar el marco. Empezar directamente con un hecho concreto o una afirmación específica. |
| **PatternES-03** | Tríada de abstractos | Lista de tres sustantivos o adjetivos abstractos (innovación, creatividad, etc.). | La IA tiende a agrupar conceptos en tripletes para sonar "completa" y equilibrada. | Elegir un concepto y desarrollarlo. Los tripletes resultan formulaicos. |
| **PatternES-04** | Tono sycofántico | Alabanzas a la pregunta del usuario o entusiasmo excesivo. | Es un artefacto de seguridad y cortesía programada de los chatbots. | Eliminar introducciones como "¡Excelente pregunta!" e ir directo a la respuesta. |
| **PatternES-05** | Énfasis metacomentario | "Cabe destacar que", "Es importante señalar que". | La IA comenta lo que va a decir en lugar de decirlo directamente. | Eliminar la muletilla y exponer el hecho de forma directa. |
| **PatternES-06** | Disclaimers de corte | Referencias a la "fecha de corte" o "modelo de lenguaje". | Es un residuo técnico de la identidad del modelo. | Eliminar completamente cualquier referencia a ser una IA. |
| **PatternES-07** | Conclusiones genéricas | Cierres vagos como "El futuro es prometedor". | La IA evita tomar posturas arriesgadas y prefiere finales optimistas y vacíos. | Cerrar con un dato específico, una acción concreta o una opinión fuerte. |
| **PatternES-08** | Atribuciones vagas | "Los expertos señalan", "Varios estudios demuestran". | Falta de fuentes específicas. La IA alucina autoridad sin dar nombres. | Citar un estudio real, un experto con nombre y apellidos, o eliminar la atribución. |
| **PatternES-09** | Lenguaje positivo extremo | Uso de adjetivos como "revolucionario" o "sin precedentes". | La IA tiende a inflar el valor emocional positivo de lo que describe. | Sustituir los elogios por cifras o descripciones factuales. |
| **PatternES-10** | Pasiva con 'ser' innecesaria | "Ha sido desarrollado por" en lugar de "Se ha desarrollado". | Influencia del inglés en los datos de entrenamiento. Suena poco natural en español. | Usar pasiva refleja o voz activa. |
| **PatternES-11** | Framing de análisis | "Procedemos a explorar", "Comencemos por analizar". | Anunciar el análisis en lugar de realizarlo. | Eliminar el anuncio y empezar el análisis directamente. |
| **PatternES-12** | Copula avoidance | "Sirve como", "Actúa como" en lugar de "Es". | Uso de equivalentes verbosos de la cópula para sonar más formal o complejo. | Usar el verbo "ser" o "estar" directamente. |
| **PatternES-13** | Pregunta retórica inicial | "¿Alguna vez te has preguntado...?" al inicio de un texto. | Gancho publicitario predecible y muy poco común en la escritura humana genuina. | Empezar con la respuesta o una afirmación, no con la pregunta. |
| **PatternES-14** | Hedging excesivo | "Podría decirse que", "En cierta medida". | Uso de calificadores que debilitan la afirmación para evitar errores. | Decirlo de forma directa o eliminar si no aporta matiz real. |
| **PatternES-15** | Paralelismo negativo | "No solo X, sino también Y". | Construcción formulaica sobreutilizada por los LLMs para estructurar ideas. | Simplificar. Desarrollar una idea directamente sin el marco comparativo. |
| **PatternES-16** | Desafíos formulaicos | "A pesar de los retos... sigue creciendo". | Estructura de "obstáculo genérico -> optimismo" muy común en textos de IA. | Nombrar el reto específico y su impacto real, o eliminar el cliché. |
| **PatternES-17** | Estructura excesiva | Cabeceras en negrita en cada punto de una lista. | Los LLMs sobre-estructuran el contenido para que parezca más legible. | Usar párrafos de prosa; reservar las listas para enumeraciones reales. |
| **PatternES-18** | Apertura formulaica | "En este artículo vamos a explorar...". | Meta-comentario sobre el texto que el lector ya está leyendo. | Eliminar y entrar en el tema en la primera frase. |
| **PatternES-19** | Cierre de chatbot | "Espero que esta información te haya sido útil". | Frases de despedida que exponen el origen artificial del texto. | Eliminar. Terminar con el contenido real. |
| **PatternES-20** | Clickbait de guía | "Todo lo que necesitas saber sobre...". | Títulos y secciones generados con fórmulas de marketing predecibles. | Escribir un título descriptivo y específico sobre el ángulo del texto. |
