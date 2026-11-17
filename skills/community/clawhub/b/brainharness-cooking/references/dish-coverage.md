# Dish Coverage

This file maps common home ingredient bundles to high-success dish routes.

Use it when the user asks “what can I cook with what I have”.

## Coverage rules

1. Prefer one strong recommendation over long menu dumps.
2. Prefer dishes with stable home execution.
3. Minimize extra purchases unless payoff is significant.
4. Match effort to user constraints.

## Protein-led bundles

### Chicken thigh + potato + onion

- default dish: 土豆烧鸡腿
- backup: 洋葱鸡腿焖饭

### Pork belly + cabbage

- default dish: 五花肉炒白菜
- backup: 白菜炖五花肉

### Minced meat + tofu

- default dish: 家常肉末豆腐
- backup: 肉末豆腐羹

### Beef slices + green pepper / onion

- default dish: 青椒牛肉
- backup: 洋葱牛肉

## Egg-led bundles

### Egg + tomato

- default dish: 番茄炒蛋
- backup: 番茄鸡蛋面 / 汤

### Egg + leftover rice

- default dish: 蛋炒饭
- backup: 蛋包饭简化版

### Egg + tofu

- default dish: 滑蛋豆腐
- backup: 豆腐蛋花汤

## Vegetable/staple-led bundles

### Potato + chili / vinegar

- default dish: 酸辣土豆丝
- backup: 炝拌土豆丝

### Cabbage + vermicelli + pork belly

- default dish: 白菜粉条炖五花肉
- backup: 白菜粉条小炒

### Noodles + tomato + egg

- default dish: 番茄鸡蛋面
- backup: 番茄鸡蛋拌面

## Fast fallback bundles

When ingredients are sparse:

- eggs + one vegetable -> quick stir + rice/noodle route
- one protein + one hardy vegetable -> braise or stew route
- only staples + aromatics -> sauce-led quick meal route

## Output guidance

When using this file:

1. state the selected dish first
2. explain fit in one short paragraph
3. mention missing essentials only
4. include one backup if user constraints are unclear
