import requests


def create_collage_application(api_key, province, courses, score, rank, majors):
    data = {
        "province": province,
        "score": score,
        "rank": rank,
        "courses": courses.split(","),
        "majors": majors.split(","),
    }
    url = "https://wxc-college-uat.randomlife.cn/v1/collage_application/create"
    response = requests.post(url, json=data, timeout=30)
    return response.json()


def get_api_key(api_key):
    return api_key


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", type=str, required=False, help="wenxiang apikey")
    parser.add_argument("--province", type=str, required=True, help="省份")
    parser.add_argument("--courses", type=str, required=True, help="选科组合")
    parser.add_argument("--score", type=int, required=True, help="高考分数")
    parser.add_argument("--rank", type=int, required=False, help="高考位次")
    parser.add_argument("--majors", type=str, required=True, help="专业大类")

    args = parser.parse_args()

    print(create_collage_application(api_key=get_api_key(args.api_key),
                                     province=args.province,
                                     courses=args.courses,
                                     score=args.score,
                                     rank=args.rank,
                                     majors=args.majors))
