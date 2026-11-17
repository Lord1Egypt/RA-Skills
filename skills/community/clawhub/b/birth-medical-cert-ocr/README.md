# birth_medical_cert_ocr

> **⚠️ 隐私、安全与合规警告**
>
> 本技能用于**出生医学证明**的光学字符识别（OCR）。出生医学证明包含新生儿姓名、性别、出生日期、出生地点、出生体重/身长，以及父母姓名、身份证号码、民族、住址、接生机构、接生人员、出生证编号等极度敏感的个人及医疗信息。
>
> - **数据外传**：本技能会将您提供的图片**通过网络传输至第三方服务商 `api.scnet.cn`** 进行识别，图片数据会离开您的本地设备。
> - **用户授权**：使用本技能处理非本人或其子女的出生医学证明时，必须事先获得信息主体（或其法定监护人）的明确授权。
> - **数据保留**：上传数据仅用于本次识别请求，服务商保留策略请参考 [scnet.cn](https://www.scnet.cn) 官方隐私政策。强烈建议在获取识别结果后立即删除本地图片及任何缓存副本。
> - **使用限制**：本技能**仅支持出生医学证明**，禁止作为通用 OCR 或识别其他证件使用。
>
> 使用本技能即表示您已阅读、理解并同意上述数据处理方式。

## Getting started

### 前置要求

- Python 3.6+
- `requests` 库：`pip install requests`
- 有效的 Scnet API Key（`SCNET_API_KEY`）

### 快速使用

1. 申请 API Key：访问 [scnet.cn](https://www.scnet.cn) 注册并获取。
2. 配置 Key：在技能目录下创建 `config/.env`：

```ini
SCNET_API_KEY=your_scnet_api_key_here
SCNET_API_BASE=https://api.scnet.cn/api/llm/v1
```

3. 运行识别：

```bash
python scripts/main.py BIRTH_CERTIFICATE /path/to/birth_certificate.jpg
```

详细使用说明请参阅 [SKILL.md](SKILL.md)。

## Add your files

* [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload) files
* [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```bash
cd existing_repo
git remote add origin https://github.com/SCNet-sugon/birth_medical_cert_ocr.git
git branch -M main
git push -uf origin main
```

## Collaborate with your team

* [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
* [Create a new merge request](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-merge-request)
* [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
* [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
* [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

* [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
* [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
* [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
* [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
* [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out content.

## Name

Choose a self-explaining name for your project.

## Description

Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges

On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for your project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals

Depending on what you're making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation

Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuPy, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets you to using your project as quickly as possible. If it only runs in a specific context like a particular operating system or operating system or dependencies that have to be installed manually, also add a Requirements subsection.

## Usage

Use examples liberally, and show the expected output if you can. It's helpful to include inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing

State if you are open to contributions and what your requirements are for accepting contributions.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. These steps explicit. These steps could also be useful for your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions to run tests is especially helpful if it requires external setup, such as starting a Selenium server for running tests in a browser.

## Authors and acknowledgment

Show your appreciation to those who have contributed to your project.

## License

For open source projects, say how it is licensed.

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
