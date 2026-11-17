# Output languages

Delivered messages may only use these 8 languages. Confirm the user's choice; if not specified, default to English or the user's interface language when it is one of the 8.

| # | Language | Code | Native name | Notes |
|---|---|---|---|---|
| 1 | English | en | English | default |
| 2 | Chinese (Mandarin, Simplified) | zh-CN | 简体中文 | |
| 3 | Spanish | es | Español | |
| 4 | Hindi | hi | हिन्दी | |
| 5 | French | fr | Français | |
| 6 | Arabic | ar | العربية | right-to-left text |
| 7 | Portuguese | pt | Português | |
| 8 | Russian | ru | Русский | |

## Fixed labels

Use the same message structure in every language, with these section labels:

| English | 中文 | Español | हिन्दी | Français | العربية | Português | Русский |
|---|---|---|---|---|---|---|---|
| Today's plan | 今日计划 | Plan de hoy | आज की योजना | Plan du jour | خطة اليوم | Plano de hoje | План на сегодня |
| Breakfast | 早餐 | Desayuno | नाश्ता | Petit-déjeuner | فطور | Café da manhã | Завтрак |
| Lunch | 午餐 | Almuerzo | दोपहर का भोजन | Déjeuner | غداء | Almoço | Обед |
| Dinner | 晚餐 | Cena | रात का खाना | Dîner | عشاء | Jantar | Ужин |
| Snack | 加餐 | Merienda | स्नैक | Collation | وجبة خفيفة | Lanche | Перекус |
| Water | 饮水 | Agua | पानी | Eau | ماء | Água | Вода |
| Workout | 训练 | Entrenamiento | कसरत | Entraînement | تمرين | Treino | Тренировка |
| Calories | 热量 | Calorías | कैलोरी | Calories | سعرات حرارية | Calorias | Калории |
| Protein | 蛋白质 | Proteína | प्रोटीन | Protéines | بروتين | Proteína | Белки |
| Carbs | 碳水 | Carbohidratos | कार्ब्स | Glucides | كربوهيدرات | Carboidratos | Углеводы |
| Fat | 脂肪 | Grasas | वसा | Lipides | دهون | Gorduras | Жиры |
| Rest day | 休息日 | Día de descanso | आराम का दिन | Jour de repos | يوم راحة | Dia de descanso | День отдыха |
| Estimated cost | 预计花费 | Costo estimado | अनुमानित खर्च | Coût estimé | التكلفة التقديرية | Custo estimado | Ориентировочная стоимость |
| Budget | 预算 | Presupuesto | बजट | Budget | الميزانية | Orçamento | Бюджет |
| Within budget | 在预算内 | Dentro del presupuesto | बजट के भीतर | Dans le budget | ضمن الميزانية | Dentro do orçamento | В пределах бюджета |
| Over budget | 超出预算 | Fuera del presupuesto | बजट से अधिक | Hors budget | تجاوز الميزانية | Acima do orçamento | Превышает бюджет |
| Weekly summary | 每周总结 | Resumen semanal | साप्ताहिक सारांश | Résumé hebdomadaire | الملخص الأسبوعي | Resumo semanal | Недельная сводка |
| Training this week | 本周训练 | Entrenamiento de esta semana | इस हफ़्ते की कसरत | Entraînement de la semaine | تدريب هذا الأسبوع | Treino desta semana | Тренировки за неделю |
| Nutrition this week | 本周饮食 | Nutrición de esta semana | इस हफ़्ते का पोषण | Alimentation de la semaine | تغذية هذا الأسبوع | Alimentação desta semana | Питание за неделю |
| Spending this week | 本周花费 | Gasto de esta semana | इस हफ़्ते का खर्च | Dépenses de la semaine | إنفاق هذا الأسبوع | Gastos desta semana | Расходы за неделю |
| Next week | 下周计划 | Próxima semana | अगला हफ़्ता | Semaine prochaine | الأسبوع القادم | Próxima semana | Следующая неделя |

## Rules

- Write the entire message in the chosen language; no mixed-language labels, except food names commonly kept in their original form.
- Dialogue scripts (opening message, three-day review, training-log follow-up) have fixed 8-language versions in [references/dialogues.md](references/dialogues.md); use them verbatim.
- Numbers and units follow the user's preference (metric kg/cm vs imperial lb/ft/in).
- If the user requests a language outside these 8, explain that the skill supports only these 8 and offer the closest match.
