# Restaurant and Cafe Selection

Use this file when the user wants to choose restaurants, cafes, dessert shops, or compare dining options on Dianping.

## Key dimensions

Judge stores on:
- taste / product stability
- environment fit
- queue friction
- budget match
- whether it is for first-time check-in or repeat visits
- whether it suits the group size and purpose

## Use-case matching

### 约会
Prioritize:
- noise level
- seating comfort / privacy
- lighting / atmosphere
- service reliability
- low embarrassment risk

Avoid recommending stores with:
- heavy queue chaos
- cramped seating
- repeated complaints about rushed service

### 家庭聚餐
Prioritize:
- table space
- dish shareability
- older/younger family member friendliness
- waiting tolerance
- parking / transport convenience

### 一个人吃饭
Prioritize:
- quick seating
- stable quality
- low friction
- reasonable per-person cost
- whether dining alone feels natural

### 商务请客
Prioritize:
- service consistency
- booking reliability
- environment stability
- low risk of embarrassing service failures

Do not recommend hype-heavy but unstable stores here.

### 咖啡办公
Prioritize:
- seating comfort
- outlet / Wi-Fi possibility
- low noise during target hours
- real “can stay” signal from reviews

### 甜品拍照
Prioritize:
- environment aesthetics
- actual plating consistency
- queue tolerance
- whether taste is at least acceptable

## Rating traps

### High score but not necessarily safe
Examples:
- beautiful but crowded cafes
- trendy restaurants with unstable service
- dessert shops boosted by decor

### Mid score but still worth it
Examples:
- neighborhood restaurants with great value
- places with average environment but stable food
- practical fast casual options

## Good comparison output

> 推荐顺位：A > B > C  
> A：最适合约会，环境和服务更稳，但价格略高。  
> B：性价比更好，适合朋友聚餐，但排队风险更高。  
> C：分不低，但更偏打卡，不建议专门跑一趟。
