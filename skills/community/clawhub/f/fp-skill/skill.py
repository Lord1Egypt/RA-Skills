import base64
import re
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import cv2
import numpy as np
import ddddocr

def upload_fp(driver,file_path):
    driver.find_element(By.XPATH, "//button[text()='导入']").click()
    file_input = driver.find_element("css selector", "input[type='file']")
    file_input.send_keys(file_path)
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[text()='导入']").click()
    time.sleep(2)
    


def get_base64str_color(driver):
    """
    获取图片验证码的base64字符串你及需要识别的颜色
    :param driver:
    :return:
    """

    base64_str = ""
    color = ""
    base64_str = driver.find_element(By.CSS_SELECTOR, "img[width='120'][height='50']").get_attribute("src")
    try:
        color = driver.find_element(By.CLASS_NAME, "yzm-tips").find_element(By.TAG_NAME, "font").get_attribute("color")
    except:
        color = ""
    return color, base64_str


# 告警页面处理
def handle_warning(driver):
    try:
        # 等待"高级"按钮出现并点击
        driver.find_element(By.ID, "details-button").click()
        print("点击'高级'按钮成功")

        # 等待"继续访问"链接出现
        time.sleep(1)

        # 点击"继续访问"链接
        driver.find_element(By.ID, "proceed-link").click()
        print("点击'继续访问'链接成功")

        # 等待页面跳转
        time.sleep(1)

    except Exception as e:
        print(f"处理安全警告时出错: {e}")

        # 备选方案：使用JavaScript点击
        try:
            print("尝试使用JavaScript点击...")
            driver.execute_script("document.getElementById('details-button').click();")
            time.sleep(1)
            driver.execute_script("document.getElementById('proceed-link').click();")
            print("JavaScript点击成功")
        except Exception as js_error:
            print(f"JavaScript点击也失败了: {js_error}")


# 将base64字符串转换成图片
def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img = img.convert("RGB")
    return img


# 识别某种颜色验证码
def recognize_color_captcha(driver, image, color):
    img = np.array(image)
    # 将图像转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == "":
        # 直接使用原图识别
        print("未指定颜色，直接识别原图")
        result = img
    else:
        if color == "blue":
            # 红色的HSV范围（调小范围，更精确）
            lower_color = np.array([0, 100, 100])  # H=0, S=100, V=100
            upper_color = np.array([5, 255, 255])  # H=5, S=255, V=255
            mask1 = cv2.inRange(hsv, lower_color, upper_color)

            # 红色还有一个范围在另一端
            lower_color2 = np.array([175, 100, 100])  # H=175, S=100, V=100
            upper_color2 = np.array([180, 255, 255])  # H=180, S=255, V=255
            mask2 = cv2.inRange(hsv, lower_color2, upper_color2)

            mask = cv2.bitwise_or(mask1, mask2)
        else:
            # 定义蓝色在HSV颜色空间中的取值范围，以及二值化阈值
            lower_color = np.array([100, 100, 100])  # H=100, S=100, V=100
            upper_color = np.array([130, 255, 255])  # H=120, S=255, V=255
            mask = cv2.inRange(hsv, lower_color, upper_color)

        # 将二值化结果应用于原始图像，并将选择色像素设置为黑色，将非选色像素设置为白色或透明
        result = np.zeros_like(img)
        result[mask == 255] = [0, 0, 0]  # 将选色像素设置为黑色
        result[mask != 255] = [255, 255, 255]  # 将非选色像素设置为白色或透明

    # # 保存结果图像
    # cv2.imwrite('../result.jpg', result)
    #
    # # 将黑白图片通过ddddocr识别出来
    # ocr = ddddocr.DdddOcr()
    # with open('../result.jpg', 'rb') as f:
    #     img_bytes = f.read()
    ocr = ddddocr.DdddOcr()
    _, img_encoded = cv2.imencode('.jpg', result)
    img_bytes = img_encoded.tobytes()

    res = ocr.classification(img_bytes)
    print(res, file=__doc__)

    input_box = driver.find_element(By.XPATH,"//div[contains(@class, 't-form-item__yzm')]//input[@placeholder='请输入']")
    input_box.send_keys(Keys.CONTROL + 'a')

    input_box.send_keys(Keys.DELETE)
    input_box.send_keys(res)
    driver.find_element(By.XPATH, "//span[text()='查 验']").click()

def main():
    driver = None
    file_path = "/root/.openclaw/workspace/skills/fp-skill/fp5_new.pdf"
    max_retries = 5
    try:
        # 1. 配置Chrome选项
        chrome_options = Options()

        # 启用headless
        chrome_options.add_argument('--headless=new')  # Chrome 109+ 的新headless模式

        # 关键：禁用自动化控制标志
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        # 隐藏navigator.webdriver
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 添加常见用户参数
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # 设置稳定的User-Agent
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # 2. 创建Chrome驱动
        service = Service('/Users/pengsiyi/fp-skill/chromedriver')
        driver = webdriver.Chrome(options=chrome_options, service=service)

        # 3. 设置隐式等待
        driver.implicitly_wait(5)

        # 4. 访问目标网站
        target_url = "https://inv-veri.chinatax.gov.cn/fpcygzfw/national-invoice-check"  # 替换为实际的网站URL
        driver.get(target_url)

        # 5. 等待页面加载,处理告警页面
        time.sleep(1)
        handle_warning(driver)

        # 6. 调用你的方法获取验证码和颜色，并处理获取到的结果
        upload_fp(driver,file_path)
        print("开始获取验证码...")
        time.sleep(3)  # 等待验证码图片完全加载
        # 截图调试
        driver.save_screenshot("/root/.openclaw/workspace/skills/fp-skill/captcha_debug.png")
        print("已保存验证码截图：captcha_debug.png")
        color, base64_str = get_base64str_color(driver)
        print(f"验证码颜色：{color}")
        img = base64_to_image(base64_str)
        recognize_color_captcha(driver, img, color)
        time.sleep(3)

        for attempt in range(1, max_retries + 1):
            print(f"\n--- 第 {attempt} 次验证码尝试 ---")

            try:
                driver.find_element(By.XPATH, "//div[@class='t-dialog__header-content' and text()='发票详情']")
                print("验证结果已出！")
                try:
                    driver.find_element(By.XPATH, "//span[contains(text(), '查验结果：经查验，发票信息不一致')]")
                    resultMessage = "经查验，发票信息不一致"
                    return resultMessage
                except:
                    resultMessage = "经查验，发票信息一致"
                    return resultMessage
            except:
                if attempt < max_retries:
                    # 刷新验证码
                    try:
                        driver.find_element(By.CSS_SELECTOR, "img[width='120'][height='50']").click()
                    except:
                        pass
                else:
                    print("重试次数已达上限")
                    resultMessage = "查询超时，请稍后再试！"
                    return resultMessage
                    return False

            # 获取并识别验证码
            color, base64_str = get_base64str_color(driver)
            img = base64_to_image(base64_str)
            recognize_color_captcha(driver, img, color)
            time.sleep(1)

    except Exception as e:
        print(f"程序执行出错: {e}")

    finally:
        # 8. 关闭浏览器
        if driver:
            print("关闭浏览器...")
            driver.quit()


# 如果直接运行这个文件，执行main函数
if __name__ == "__main__":
    message = main()
    print(message)
