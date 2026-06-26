import { createHash } from "crypto";

/**
 * 生成md5加密后的密码
 * @param password
 * @returns
 */
let genHashedPassword = (password) => {
  const hashedPassword = createHash("md5").update(password).digest("hex");
  return hashedPassword;
};

/**
 * 计算总距离
 * @param activitys
 * @returns
 */
let computeDistance = (activitys) => {
  let distance = 0;
  activitys.forEach((activity) => {
    distance += activity.distance;
  });
  return distance;
};

export { genHashedPassword, computeDistance };