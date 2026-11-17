from setuptools import setup

setup(
    name='baidu-youjia-car',
    version='1.1.0',
    py_modules=['youjia_client', 'send_code', 'create_key', 'save_config'],
    package_dir={'': 'scripts'},
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'youjia-send-code=send_code:main',
            'youjia-create-key=create_key:main',
            'youjia-save-config=save_config:main',
        ],
    },
)
